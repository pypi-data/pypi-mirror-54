# Copyright 2019 The TensorFlow-Determinism Authors. All Rights Reserved
#
# _new_biad_add_1_14() derived from source in
# https://github/tensorflow/tensorflow and therefore
# Copyright 2019 The TensorFlow Authors. All Rights Reserved
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
# ========================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re
import sys

import tensorflow as tf
from tensorflow.python.eager import context
from tensorflow.python.framework import dtypes
from tensorflow.python.framework import ops
from tensorflow.python.keras import backend as K
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import nn
from tensorflow.python.ops import nn_ops

from .version import __version__

def _patch():
  """Patches TensorFlow to increase determinism when running on GPUs.

    Calling this method either before or after explicitly importing TensorFlow,
    but always before constructing any graphs, will increase the determinsism
    when running on GPUs.

    Returns: nothing

    Raises:
      ValueError if a patch is not available for the installed version of
      TensorFlow.
  """
  if os.environ.get('NVIDIA_TENSORFLOW_VERSION'):
    raise Exception("tfdeterminism: TensorFlow inside NGC containers does not "
                    "require patching")
  tf_version = tf.version.VERSION
  if re.match("(1\.(14|15)|2\.0)", tf_version):
    os.environ['TF_CUDNN_DETERMINISTIC'] = '1'
    _patch_bias_add()
    print("TensorFlow version %s has been patched "
          "using tfdeterminism version %s" %
          (tf_version, __version__), file=sys.stderr)
  else:
    raise Exception("tfdeterminism: No patch available "
                    "for version %s of TensorFlow" % tf_version)

def _patch_bias_add():
  tf.nn.bias_add = _new_bias_add_1_14 # access via public API
  nn.bias_add = _new_bias_add_1_14 # called from tf.keras.layers.convolutional.Conv
  nn_ops.bias_add = _new_bias_add_1_14 # called from tests

# The original, pre-patched method can be viewed at
# https://github.com/tensorflow/tensorflow/blob/v1.14.0/tensorflow/python/ops/nn_ops.py#L2628
def _new_bias_add_1_14(value, bias, data_format=None, name=None):
  """Adds `bias` to `value`.

  This is (mostly) a special case of `tf.add` where `bias` is restricted to 1-D.
  Broadcasting is supported, so `value` may have any number of dimensions.
  Unlike `tf.add`, the type of `bias` is allowed to differ from `value` in the
  case where both types are quantized.

  Args:
    value: A `Tensor` with type `float`, `double`, `int64`, `int32`, `uint8`,
      `int16`, `int8`, `complex64`, or `complex128`.
    bias: A 1-D `Tensor` with size matching the channel dimension of `value`.
      Must be the same type as `value` unless `value` is a quantized type,
      in which case a different quantized type may be used.
    data_format: A string. 'N...C' and 'NC...' are supported. If `None` (the
      default) is specified then 'N..C' is assumed.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` with the same type as `value`.

  Raises:
    ValueError if data format is unrecognized, if `value` has less than two
    dimensions when `data_format` is 'N..C'/`None` or `value` has less
    then three dimensions when `data_format` is `NC..`, if `bias` does not
    have exactly one dimension (is a vector), or if the size of `bias`
    does not match the size of the channel dimension of `value`.
  """
  with ops.name_scope(name, "BiasAdd", [value, bias]) as name:
    if data_format is not None:
      if data_format.startswith("NC"):
        data_format = "NCHW"
      elif data_format.startswith("N") and data_format.endswith("C"):
        data_format = "NHWC"
      else:
        raise ValueError("data_format must be of the form `N...C` or `NC...`")

    if not context.executing_eagerly():
      value = ops.convert_to_tensor(value, name="input")
      bias = ops.convert_to_tensor(bias, dtype=value.dtype, name="bias")

    if data_format == 'NCHW':
      broadcast_shape_head = [1, array_ops.size(bias)]
      broadcast_shape_tail = array_ops.ones(array_ops.rank(value) - 2,
                                            dtype=dtypes.int32)
      broadcast_shape = array_ops.concat(
          [broadcast_shape_head, broadcast_shape_tail], 0)
      return math_ops.add(
          value, array_ops.reshape(bias, broadcast_shape), name=name)
    else: # data_format == 'NHWC' or data_format == None
      return math_ops.add(value, bias, name=name)
