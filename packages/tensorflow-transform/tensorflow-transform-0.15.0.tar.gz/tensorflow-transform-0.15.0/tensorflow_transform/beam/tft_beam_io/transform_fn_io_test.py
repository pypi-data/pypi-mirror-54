# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for transform_fn_io."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

# GOOGLE-INITIALIZATION

import apache_beam as beam
from apache_beam.testing import util as beam_test_util
import tensorflow as tf

import tensorflow_transform as tft
from tensorflow_transform.beam.tft_beam_io import beam_metadata_io
from tensorflow_transform.beam.tft_beam_io import transform_fn_io
from tensorflow_transform.beam.tft_beam_io import test_metadata
from tensorflow_transform.tf_metadata import metadata_io

from tensorflow.python.lib.io import file_io


class BeamMetadataIoTest(tf.test.TestCase):

  def testReadTransformFn(self):
    path = self.get_temp_dir()
    # NOTE: we don't need to create or write to the transform_fn directory since
    # ReadTransformFn never inspects this directory.
    transform_fn_dir = os.path.join(
        path, tft.TFTransformOutput.TRANSFORM_FN_DIR)
    transformed_metadata_dir = os.path.join(
        path, tft.TFTransformOutput.TRANSFORMED_METADATA_DIR)
    metadata_io.write_metadata(test_metadata.COMPLETE_METADATA,
                               transformed_metadata_dir)

    with beam.Pipeline() as pipeline:
      saved_model_dir_pcoll, metadata = (
          pipeline | transform_fn_io.ReadTransformFn(path))
      beam_test_util.assert_that(
          saved_model_dir_pcoll, beam_test_util.equal_to([transform_fn_dir]),
          label='AssertSavedModelDir')
      # NOTE: metadata is currently read in a non-deferred manner.
      self.assertEqual(metadata, test_metadata.COMPLETE_METADATA)

  def testWriteTransformFn(self):
    transform_output_dir = os.path.join(self.get_temp_dir(), 'output')

    with beam.Pipeline() as pipeline:
      # Create an empty directory for the source saved model dir.
      saved_model_dir = os.path.join(self.get_temp_dir(), 'source')
      file_io.recursive_create_dir(saved_model_dir)
      saved_model_dir_pcoll = (
          pipeline | 'CreateSavedModelDir' >> beam.Create([saved_model_dir]))
      # Combine test metadata with a dict of PCollections resolving futures.
      deferred_metadata = pipeline | 'CreateDeferredMetadata' >> beam.Create(
          [test_metadata.COMPLETE_METADATA])
      metadata = beam_metadata_io.BeamDatasetMetadata(
          test_metadata.INCOMPLETE_METADATA, deferred_metadata)

      _ = ((saved_model_dir_pcoll, metadata)
           | transform_fn_io.WriteTransformFn(transform_output_dir))

    # Test reading with TFTransformOutput
    tf_transform_output = tft.TFTransformOutput(transform_output_dir)
    metadata = tf_transform_output.transformed_metadata
    self.assertEqual(metadata, test_metadata.COMPLETE_METADATA)

    transform_fn_dir = tf_transform_output.transform_savedmodel_dir
    self.assertTrue(file_io.file_exists(transform_fn_dir))
    self.assertTrue(file_io.is_directory(transform_fn_dir))

if __name__ == '__main__':
  tf.test.main()
