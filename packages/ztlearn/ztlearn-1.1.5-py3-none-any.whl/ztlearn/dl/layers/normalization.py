# -*- coding: utf-8 -*-

import numpy as np

from .base import Layer
from ztlearn.optimizers import OptimizationFunction as optimizer


class BatchNormalization(Layer):

    def __init__(self, eps = 0.01, momentum = 0.99):
        self.eps      = eps
        self.momentum = momentum

        self.running_var      = None
        self.running_mean     = None
        self.optimizer_kwargs = None

        self.is_trainable = True

    @property
    def trainable(self):
        return self.is_trainable

    @trainable.setter
    def trainable(self, is_trainable):
        self.is_trainable = is_trainable

    @property
    def weight_optimizer(self):
        return self.optimizer_kwargs

    @weight_optimizer.setter
    def weight_optimizer(self, optimizer_kwargs = {}):
        self.optimizer_kwargs = optimizer_kwargs

    @property
    def layer_parameters(self):
        return sum([np.prod(param.shape) for param in [self.gamma, self.beta]])

    @property
    def output_shape(self):
        return self.input_shape

    def prep_layer(self):
        self.gamma = np.ones(self.input_shape)
        self.beta  = np.zeros(self.input_shape)

    def pass_forward(self, inputs, train_mode = True, **kwargs):
        if self.running_var is None:
            self.running_var = np.var(inputs, axis = 0)

        if self.running_mean is None:
            self.running_mean = np.mean(inputs, axis = 0)

        if train_mode and self.is_trainable:
            self.var  = np.var(inputs, axis = 0)
            self.mean = np.mean(inputs, axis = 0)

            self.running_var  = self.momentum * self.running_var  + (1 - self.momentum) * self.var
            self.running_mean = self.momentum * self.running_mean + (1 - self.momentum) * self.mean
        else:
            self.var  = self.running_var
            self.mean = self.running_mean

        self.input_mean = inputs - self.mean
        self.inv_stddev = np.reciprocal(np.sqrt(self.var + self.eps))
        self.input_norm = self.input_mean * self.inv_stddev

        return self.gamma * self.input_norm + self.beta

    def pass_backward(self, grad, epoch_num, batch_num, batch_size):
        dinput_norm = grad * self.gamma

        if self.is_trainable:

            dbeta  = np.sum(grad, axis = 0)
            dgamma = np.sum(grad * self.input_norm, axis = 0)

            self.gamma = optimizer(self.weight_optimizer).update(self.gamma, dgamma, epoch_num, batch_num, batch_size)
            self.beta  = optimizer(self.weight_optimizer).update(self.beta, dbeta, epoch_num, batch_num, batch_size)

        # endif self.is_trainable

        dinput = np.divide(1., grad.shape[0]) * self.inv_stddev * (grad.shape[0] * dinput_norm - np.sum(dinput_norm, axis = 0) - self.input_norm * np.sum(dinput_norm * self.input_norm, axis = 0))

        return dinput


class LayerNormalization1D(Layer):

    def __init__(self, eps = 1e-5):
        self.eps              = eps
        self.optimizer_kwargs = None

        self.is_trainable = True

    @property
    def trainable(self):
        return self.is_trainable

    @trainable.setter
    def trainable(self, is_trainable):
        self.is_trainable = is_trainable

    @property
    def weight_optimizer(self):
        return self.optimizer_kwargs

    @weight_optimizer.setter
    def weight_optimizer(self, optimizer_kwargs = {}):
        self.optimizer_kwargs = optimizer_kwargs

    @property
    def output_shape(self):
        return self.input_shape

    def prep_layer(self):
        self.gamma = np.ones(self.input_shape) # * 0.2 (reduce gamma to 0.2 incase of NaNs)
        self.beta  = np.zeros(self.input_shape)

    def pass_forward(self, inputs, train_mode = True, **kwargs):
        self.mean = np.mean(inputs, axis = -1, keepdims = True)
        self.std  = np.std(inputs,  axis = -1, keepdims = True)

        self.input_mean = inputs - self.mean
        self.inv_stddev = np.reciprocal(self.std + self.eps)
        self.input_norm = self.input_mean * self.inv_stddev

        return self.input_norm * self.gamma + self.beta

    def pass_backward(self, grad, epoch_num, batch_num, batch_size):
        dinput_norm = grad * self.gamma

        if self.is_trainable:

            dbeta  = np.sum(grad, axis = 0)
            dgamma = np.sum(grad * self.input_norm, axis = 0)

            self.gamma = optimizer(self.weight_optimizer).update(self.gamma, dgamma, epoch_num, batch_num, batch_size)
            self.beta  = optimizer(self.weight_optimizer).update(self.beta, dbeta, epoch_num, batch_num, batch_size)

        # endif self.is_trainable

        dinput = np.divide(1., grad.shape[0]) * self.inv_stddev * (grad.shape[0] * dinput_norm - np.sum(dinput_norm, axis = 0) - self.input_norm * np.sum(dinput_norm * self.input_norm, axis = 0))

        return dinput
