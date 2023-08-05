# -*- coding: utf-8 -*-

import numpy as np

from .base import Layer
from ztlearn.initializers import InitializeWeights as init
from ztlearn.optimizers import OptimizationFunction as optimizer
from ztlearn.activations import ActivationFunction as activation


class Activation(Layer):

    def __init__(self, function_name, input_shape = None, **kwargs):
        self.input_shape     = input_shape
        self.activation_name = function_name

        allowed_kwargs = {'alpha'}
        for kwrd in kwargs:
            if kwrd not in allowed_kwargs:
                raise TypeError('Unexpected keyword argument passed to activation: ' + str(kwrd))

        self.activation_func = activation(self.activation_name, kwargs)

        self.is_trainable = True

    @property
    def trainable(self):
        return self.is_trainable

    @trainable.setter
    def trainable(self, is_trainable):
        self.is_trainable = is_trainable

    @property
    def output_shape(self):
        return self.input_shape

    @property
    def layer_name(self):
        return "Activation: {}".format(" ".join(self.activation_name.upper().split("_")))

    def prep_layer(self): pass

    def pass_forward(self, input_signal, train_mode = True, **kwargs):
        self.input_signal = input_signal
        return self.activation_func.forward(input_signal)

    def pass_backward(self, grad, epoch_num, batch_num, batch_size):
        return grad * self.activation_func.backward(self.input_signal)


class Dense(Layer):

    def __init__(self, units, activation = None, input_shape = None):
        self.units       = units
        self.activation  = activation
        self.input_shape = input_shape

        self.bias             = None
        self.weights          = None
        self.init_method      = None
        self.optimizer_kwargs = None

        self.is_trainable = True

    @property
    def trainable(self):
        return self.is_trainable

    @trainable.setter
    def trainable(self, is_trainable):
        self.is_trainable = is_trainable

    @property
    def weight_initializer(self):
        return self.init_method

    @weight_initializer.setter
    def weight_initializer(self, init_method):
        self.init_method = init_method

    @property
    def weight_optimizer(self):
        return self.optimizer_kwargs

    @weight_optimizer.setter
    def weight_optimizer(self, optimizer_kwargs = {}):
        self.optimizer_kwargs = optimizer_kwargs

    @property
    def layer_activation(self):
        return self.activation

    @layer_activation.setter
    def layer_activation(self, activation):
        self.activation = activation

    @property
    def layer_parameters(self):
        return sum([np.prod(param.shape) for param in [self.weights, self.bias]])

    @property
    def output_shape(self):
        return (self.units,)

    def prep_layer(self):
        self.kernel_shape = (self.input_shape[0], self.units)
        self.weights      = init(self.weight_initializer).initialize_weights(self.kernel_shape)
        self.bias         = np.zeros((1, self.units))
        # @@DEPRECATED: initialize bias using the chosen weight initializers
        # self.bias       = init(self.weight_initializer).initialize_weights((1, self.units))

    def pass_forward(self, inputs, train_mode = True):
        self.inputs = inputs

        return inputs @ self.weights + self.bias

    def pass_backward(self, grad, epoch_num, batch_num, batch_size):
        prev_weights = self.weights

        if self.is_trainable:

            dweights = self.inputs.T @ grad
            dbias    = np.sum(grad, axis = 0, keepdims = True)

            self.weights = optimizer(self.weight_optimizer).update(self.weights, dweights, epoch_num, batch_num, batch_size)
            self.bias    = optimizer(self.weight_optimizer).update(self.bias, dbias, epoch_num, batch_num, batch_size)

        # endif self.is_trainable

        return grad @ prev_weights.T


class Dropout(Layer):

    def __init__(self, drop = 0.5):
        self.drop = drop
        self.mask = None

        self.is_trainable = True

    @property
    def trainable(self):
        return self.is_trainable

    @trainable.setter
    def trainable(self, is_trainable):
        self.is_trainable = is_trainable

    @property
    def output_shape(self):
        return self.input_shape

    def prep_layer(self): pass

    def pass_forward(self, inputs, train_mode = True, **kwargs):
        if 0. < self.drop < 1.:
            keep_prob = (1 - self.drop)
            if train_mode:
                self.mask = np.random.binomial(1, keep_prob, size = inputs.shape) / keep_prob
                keep_prob = self.mask
            return inputs * keep_prob
        else:
            return inputs

    def pass_backward(self, grad, epoch_num, batch_num, batch_size):
        if 0. < self.drop < 1.:
            return grad * self.mask
        else:
            return grad


class Flatten(Layer):

    def __init__(self, input_shape = None):
        self.input_shape = input_shape
        self.prev_shape  = None

        self.is_trainable = True

    @property
    def trainable(self):
        return self.is_trainable

    @trainable.setter
    def trainable(self, is_trainable):
        self.is_trainable = is_trainable

    @property
    def output_shape(self):
        return (np.prod(self.input_shape),)

    def prep_layer(self): pass

    def pass_forward(self, inputs, train_mode = True, **kwargs):
        self.prev_shape = inputs.shape
        return np.reshape(inputs, (inputs.shape[0], -1))

    def pass_backward(self, grad, epoch_num, batch_num, batch_size):
        return np.reshape(grad, self.prev_shape)


class UpSampling2D(Layer):

    def __init__(self, size = (2, 2), input_shape = None):
        self.h_scale, self.w_scale = size[0], size[1]
        self.input_shape           = input_shape
        self.prev_shape            = None

        self.is_trainable = True

    @property
    def trainable(self):
        return self.is_trainable

    @trainable.setter
    def trainable(self, is_trainable):
        self.is_trainable = is_trainable

    @property
    def output_shape(self):
        input_depth, input_height, input_width = self.input_shape
        return input_depth, self.h_scale * input_height, self.w_scale * input_width

    def prep_layer(self): pass

    def pass_forward(self, inputs, train_mode = True, **kwargs):
        self.prev_shape = inputs.shape
        return np.repeat(np.repeat(inputs, self.h_scale, axis = 2), self.w_scale, axis = 3)

    def pass_backward(self, grad, epoch_num, batch_num, batch_size):
        grad = grad[:, :, ::self.h_scale, ::self.w_scale]
        assert grad.shape == self.prev_shape, 'grad shape incorrect'

        return grad


class Reshape(Layer):

    def __init__(self, target_shape, input_shape = None):
        self.target_shape = target_shape
        self.input_shape  = input_shape
        self.prev_shape   = None

        self.is_trainable = True

    @property
    def trainable(self):
        return self.is_trainable

    @trainable.setter
    def trainable(self, is_trainable):
        self.is_trainable = is_trainable

    @property
    def output_shape(self):
        return self.target_shape

    def prep_layer(self): pass

    def pass_forward(self, inputs, train_mode = True, **kwargs):
        self.prev_shape = inputs.shape
        return np.reshape(inputs, (inputs.shape[0],) + self.target_shape)

    def pass_backward(self, grad, epoch_num, batch_num, batch_size):
        return np.reshape(grad, self.prev_shape)
