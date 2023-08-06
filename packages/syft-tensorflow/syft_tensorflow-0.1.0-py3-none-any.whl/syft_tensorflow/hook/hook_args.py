"""Hook args implementation for TensorFLow.
Implements and registers hook_args functionality for syft-tensorflow objects.
See syft/generic/frameworks/hook/hook_args.py for the core implementation.
"""

import tensorflow as tf
import numpy as np

from tensorflow.python.framework.ops import EagerTensor
from syft.exceptions import PureFrameworkTensorFoundError
from tensorflow.python.ops.resource_variable_ops import ResourceVariable
from syft.generic.frameworks.hook.hook_args import (
    register_ambiguous_method,
    register_backward_func,
    register_forward_func,
    register_type_rule,
    one,
)

from syft_tensorflow.syft_types import TensorFlowTensor


type_rule = {
    tf.Tensor: one,
    tf.Variable: one,
    TensorFlowTensor: one,
    EagerTensor: one,
    ResourceVariable: one,
    np.ndarray: lambda x: 0,
    tf.keras.layers.Layer: one,
    tf.keras.models.Model:one,
}


def default_forward(i):
    if hasattr(i, "child"):
        return i.child

    return (_ for _ in ()).throw(PureFrameworkTensorFoundError)


forward_func = {
    tf.Tensor: default_forward,
    tf.Variable: default_forward,
    ResourceVariable: default_forward,
    EagerTensor: default_forward,
    tf.keras.layers.Layer: default_forward,
    tf.keras.models.Model: default_forward,

}
backward_func = {
    tf.Tensor: lambda i: i.wrap(type=tf.constant, value=[]),
    tf.Variable: lambda i: i.wrap(type=tf.Variable, initial_value=[]),
    ResourceVariable: lambda i: i.wrap(type=tf.Variable, initial_value=[]),
    EagerTensor: lambda i: i.wrap(type=tf.constant, value=[]),
    tf.keras.layers.Layer: lambda i: i.wrap(),
    tf.keras.models.Model: lambda i: i.wrap(),
}
ambiguous_methods = {"__getitem__", "__setitem__"}

register_ambiguous_method(*ambiguous_methods)
register_type_rule(type_rule)
register_forward_func(forward_func)
register_backward_func(backward_func)
