# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Decode CSV records into in-memory representation for tf data validation."""

from __future__ import absolute_import
from __future__ import division

from __future__ import print_function

import collections
import csv
import apache_beam as beam
import numpy as np
import six
from tensorflow_data_validation import constants
from tensorflow_data_validation import types
from tensorflow_data_validation.pyarrow_tf import pyarrow as pa
from tensorflow_data_validation.pyarrow_tf import tensorflow as tf
from tensorflow_data_validation.utils import batch_util
from tensorflow_data_validation.types_compat import Dict, List, Optional, Text

from tensorflow_metadata.proto.v0 import schema_pb2
from tensorflow_metadata.proto.v0 import statistics_pb2

# Named tuple with column name and its type.
ColumnInfo = collections.namedtuple('ColumnInfo', ['name', 'type'])


# TODO(b/111831548): Add support for a secondary delimiter to parse
# value lists.
@beam.typehints.with_input_types(types.BeamCSVRecord)
@beam.typehints.with_output_types(pa.Table)
class DecodeCSV(beam.PTransform):
  """Decodes CSV records into Arrow tables.

  Currently we assume each column in the input CSV has only a single value.
  """

  def __init__(
      self,
      column_names                         ,
      delimiter       = ',',
      skip_blank_lines       = True,
      schema                              = None,
      infer_type_from_schema       = False,
      desired_batch_size      = constants.DEFAULT_DESIRED_INPUT_BATCH_SIZE
  ):
    """Initializes the CSV decoder.

    Args:
      column_names: List of feature names. Order must match the order in the CSV
        file.
      delimiter: A one-character string used to separate fields.
      skip_blank_lines: A boolean to indicate whether to skip over blank lines
        rather than interpreting them as missing values.
      schema: An optional schema of the input data.
      infer_type_from_schema: A boolean to indicate whether the feature types
        should be inferred from the schema. If set to True, an input schema must
        be provided.
      desired_batch_size: Batch size. The output Arrow tables will have as many
        rows as the `desired_batch_size`.
    """
    if not isinstance(column_names, list):
      raise TypeError('column_names is of type %s, should be a list' %
                      type(column_names).__name__)
    self._column_names = column_names
    self._delimiter = delimiter
    self._skip_blank_lines = skip_blank_lines
    self._schema = schema
    self._infer_type_from_schema = infer_type_from_schema
    self._desired_batch_size = desired_batch_size

  def expand(self, lines                         ):
    """Decodes the input CSV records into Arrow tables.

    Args:
      lines: A PCollection of strings representing the lines in the CSV file.

    Returns:
      A PCollection of Arrow tables.
    """
    return (lines
            | 'DecodeCSVToDict' >> DecodeCSVToDict(
                column_names=self._column_names,
                delimiter=self._delimiter,
                skip_blank_lines=self._skip_blank_lines,
                schema=self._schema,
                infer_type_from_schema=self._infer_type_from_schema)
            | 'BatchExamplesToArrowTables' >>
            batch_util.BatchExamplesToArrowTables(
                desired_batch_size=self._desired_batch_size))


@beam.typehints.with_input_types(types.BeamCSVRecord)
@beam.typehints.with_output_types(types.BeamExample)
class DecodeCSVToDict(beam.PTransform):
  """Decodes CSV records into an in-memory dict representation.

  Currently we assume each column has only a single value.
  """

  def __init__(
      self,
      column_names                         ,
      delimiter       = ',',
      skip_blank_lines       = True,
      schema                              = None,
      infer_type_from_schema       = False,
  ):
    """Initializes the CSV decoder.

    Args:
      column_names: List of feature names. Order must match the order in the CSV
        file.
      delimiter: A one-character string used to separate fields.
      skip_blank_lines: A boolean to indicate whether to skip over blank lines
        rather than interpreting them as missing values.
      schema: An optional schema of the input data.
      infer_type_from_schema: A boolean to indicate whether the feature types
        should be inferred from the schema. If set to True, an input schema must
        be provided.
    """
    if not isinstance(column_names, list):
      raise TypeError('column_names is of type %s, should be a list' %
                      type(column_names).__name__)
    self._column_names = column_names
    self._delimiter = delimiter
    self._skip_blank_lines = skip_blank_lines
    self._schema = schema
    self._infer_type_from_schema = infer_type_from_schema

  def expand(self, lines                         ):
    """Decodes the input CSV records into an in-memory dict representation.

    Args:
      lines: A PCollection of strings representing the lines in the CSV file.

    Returns:
      A PCollection of dicts representing the CSV records.
    """
    input_rows = (
        lines | 'ParseCSVRecords' >> beam.Map(
            CSVParser(delimiter=self._delimiter).parse))

    if self._infer_type_from_schema:
      column_info = _get_feature_types_from_schema(self._schema,
                                                   self._column_names)
    else:
      # TODO(b/72746442): Consider using a DeepCopy optimization similar to TFT.
      # Do first pass to infer the feature types.
      column_info = (
          input_rows | 'InferFeatureTypes' >> beam.CombineGlobally(
              _FeatureTypeInferrer(
                  column_names=self._column_names,
                  skip_blank_lines=self._skip_blank_lines)))
      column_info = beam.pvalue.AsSingleton(column_info)

    # Do second pass to generate the in-memory dict representation.
    return (input_rows
            | 'CreateInMemoryDict' >> beam.FlatMap(
                _make_example_dict,
                skip_blank_lines=self._skip_blank_lines,
                column_info=column_info))


def _get_feature_types_from_schema(
    schema                   ,
    column_names                         )                    :
  """Get statistics feature types from the input schema."""
  schema_type_to_stats_type = {
      schema_pb2.INT: statistics_pb2.FeatureNameStatistics.INT,
      schema_pb2.FLOAT: statistics_pb2.FeatureNameStatistics.FLOAT,
      schema_pb2.BYTES: statistics_pb2.FeatureNameStatistics.STRING
  }
  feature_type_map = {}
  for feature in schema.feature:
    feature_type_map[feature.name] = schema_type_to_stats_type[feature.type]

  return [
      ColumnInfo(col_name, feature_type_map.get(col_name, None))
      for col_name in column_names
  ]


# The code for parsing CSV records has been copied from https://github.com/tensorflow/transform/blob/master/tensorflow_transform/coders/csv_coder.py  # pylint: disable=line-too-long
# TODO(b/112061319): Clean up the parsing logic to use the CSV coder from TFT
# once it adds support for an optional schema.
class _LineGenerator(object):
  """A csv line generator that allows feeding lines to a csv.DictReader."""

  def __init__(self):
    self._lines = []

  def push_line(self, line                 ):
    # This API currently supports only one line at a time.
    assert not self._lines
    self._lines.append(line)

  def __iter__(self):
    return self

  def __next__(self)                   :
    """Gets the next line to process."""
    # This API currently supports only one line at a time.
    num_lines = len(self._lines)
    if num_lines == 0:
      raise ValueError('No line was found.')

    assert num_lines == 1, 'Unexpected number of lines %d' % num_lines
    # This doesn't maintain insertion order to the list, which is fine
    # because the list has only 1 element. If there were more and we wanted
    # to maintain order and timecomplexity we would switch to deque.popleft.
    return self._lines.pop()

  next = __next__


class CSVParser(object):
  """A parser to parse CSV formatted data."""

  class _ReaderWrapper(object):
    """A wrapper for csv.reader to make it picklable."""

    def __init__(self, delimiter     ):
      self._state = (delimiter)
      self._line_generator = _LineGenerator()
      self._reader = csv.reader(self._line_generator, delimiter=delimiter)

    def read_record(self, csv_string                 )               :
      """Reads out bytes for PY2 and Unicode for PY3."""
      if six.PY2:
        # TODO(caveness): Test performance impact of removing nested dots
        # throughout file and possibly update decoder based on results.
        line = tf.compat.as_bytes(csv_string)
      else:
        line = tf.compat.as_text(csv_string)
      self._line_generator.push_line(line)
      output = next(self._reader)
      return [tf.compat.as_bytes(x) for x in output]

    def __getstate__(self):
      return self._state

    def __setstate__(self, state):
      self.__init__(*state)

  def __init__(self, delimiter     )        :
    """Initializes CSVParser.

    Args:
      delimiter: A one-character string used to separate fields.
    """
    self._delimiter = delimiter
    self._reader = self._ReaderWrapper(delimiter)

  def __reduce__(self):
    return CSVParser, (self._delimiter,)

  def parse(self, csv_string                 )                       :
    """Parse a CSV record into a list of strings."""
    return self._reader.read_record(csv_string)


def _make_example_dict(row                     , skip_blank_lines      ,
                       column_info                  )                       :
  """Create the in-memory representation from the CSV record.

  Args:
    row: List of cell values in a CSV record.
    skip_blank_lines: A boolean to indicate whether to skip over blank lines
      rather than interpreting them as missing values.
    column_info: List of tuples specifying column name and its type.

  Returns:
    A list containing the in-memory dict representation of the input CSV row.
  """
  if not row and skip_blank_lines:
    return []

  result = {}
  for index, field in enumerate(row):
    feature_name, feature_type = column_info[index]
    if not field:
      # If the field is an empty string, add the feature key with value as None.
      result[feature_name] = None
    elif feature_type == statistics_pb2.FeatureNameStatistics.INT:
      result[feature_name] = np.asarray([int(field)], dtype=np.int64)
    elif feature_type == statistics_pb2.FeatureNameStatistics.FLOAT:
      result[feature_name] = np.asarray([float(field)], dtype=np.float32)
    elif feature_type == statistics_pb2.FeatureNameStatistics.STRING:
      result[feature_name] = np.asarray([field], dtype=np.object)
    else:
      raise TypeError('Cannot determine the type of column %s.' % feature_name)
  return [result]


_INT64_MIN = np.iinfo(np.int64).min
_INT64_MAX = np.iinfo(np.int64).max


def _infer_value_type(value               )                                   :
  """Infer feature type from the input value."""
  # If the value is an empty string, we can set the feature type to be
  # either FLOAT or STRING. We conservatively set it to be FLOAT.
  if not value:
    return statistics_pb2.FeatureNameStatistics.FLOAT

  # Check if the value is of type INT.
  try:
    if _INT64_MIN <= int(value) <= _INT64_MAX:
      return statistics_pb2.FeatureNameStatistics.INT
    # We infer STRING type when we have long integer values.
    return statistics_pb2.FeatureNameStatistics.STRING
  except ValueError:
    # If the type is not INT, we next check for FLOAT type (according to our
    # type hierarchy). If we can convert the string to a float value, we
    # fix the type to be FLOAT. Else we resort to STRING type.
    try:
      float(value)
    except ValueError:
      return statistics_pb2.FeatureNameStatistics.STRING
    return statistics_pb2.FeatureNameStatistics.FLOAT


@beam.typehints.with_input_types(beam.typehints.List[types.BeamCSVCell])
@beam.typehints.with_output_types(beam.typehints.List[ColumnInfo])
class _FeatureTypeInferrer(beam.CombineFn):
  """Class to infer feature types as a beam.CombineFn."""

  def __init__(self, column_names                         ,
               skip_blank_lines      )        :
    """Initializes a feature type inferrer combiner."""
    self._column_names = column_names
    self._skip_blank_lines = skip_blank_lines

  def create_accumulator(
      self)                                                            :  # pytype: disable=invalid-annotation
    """Creates an empty accumulator to keep track of the feature types."""
    return {}

  def add_input(
      self,
      accumulator                                                          ,
      input_row                     
  )                                                            :
    """Updates the feature types in the accumulator using the input row.

    Args:
      accumulator: A dict containing the already inferred feature types.
      input_row: A list containing feature values of a CSV record.

    Returns:
      A dict containing the updated feature types based on input row.

    Raises:
      ValueError: If the columns do not match the specified csv headers.
    """
    # If the row is empty and we don't want to skip blank lines,
    # add an empty string to each column.
    if not input_row and not self._skip_blank_lines:
      input_row = ['' for _ in six.moves.range(len(self._column_names))]
    elif input_row and len(input_row) != len(self._column_names):
      raise ValueError('Columns do not match specified csv headers: %s -> %s' %
                       (self._column_names, input_row))

    # Iterate over each feature value and update the type.
    for index, field in enumerate(input_row):
      feature_name = self._column_names[index]

      # Get the already inferred type of the feature.
      previous_type = accumulator.get(feature_name, None)
      # Infer the type from the current feature value.
      current_type = _infer_value_type(field)

      # If the type inferred from the current value is higher in the type
      # hierarchy compared to the already inferred type, we update the type.
      # The type hierarchy is,
      #   INT (level 0) --> FLOAT (level 1) --> STRING (level 2)
      if previous_type is None or current_type > previous_type:
        accumulator[feature_name] = current_type
    return accumulator

  def merge_accumulators(
      self, accumulators       
                                                                   
  )                                                            :
    """Merge the feature types inferred from the different partitions.

    Args:
      accumulators: A list of dicts containing the feature types inferred from
        the different partitions of the data.

    Returns:
      A dict containing the merged feature types.
    """
    result = {}
    for shard_types in accumulators:
      # Merge the types inferred in each partition using the type hierarchy.
      # Specifically, whenever we observe a type higher in the type hierarchy
      # we update the type.
      for feature_name, feature_type in shard_types.items():
        if feature_name not in result or feature_type > result[feature_name]:
          result[feature_name] = feature_type
    return result

  def extract_output(
      self,
      accumulator                                                          
  )                    :
    """Return a list of tuples containing the column info."""
    return [
        ColumnInfo(col_name, accumulator.get(col_name, None))
        for col_name in self._column_names
    ]
