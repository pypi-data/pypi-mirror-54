# -*- coding: utf-8 -*-

import numpy as np

from .decayers import DecayFunction as decayer


class Optimizer(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_learning_rate(self, current_epoch):
        self.min_lr     = self.min_lr     if hasattr(self, 'min_lr')     else 0
        self.max_lr     = self.max_lr     if hasattr(self, 'max_lr')     else np.inf
        self.decay_rate = self.decay_rate if hasattr(self, 'decay_rate') else 1e-6
        self.decay_func = self.decay_func if hasattr(self, 'decay_func') else 'inverse'
        self.decay_lr   = self.decay_lr   if hasattr(self, 'decay_lr')   else True

        if self.decay_lr is False: return self.lr

        if current_epoch == 1: return self.lr

        if hasattr(self, 'step_size') and isinstance(self.step_size, (int, np.integer)):

            return decayer(self.lr,
                                    self.decay_func,
                                    self.decay_rate,
                                    current_epoch,
                                    self.min_lr,
                                    self.max_lr,
                                    self.step_size).decompose

        return decayer(self.lr,
                                self.decay_func,
                                self.decay_rate,
                                current_epoch,
                                self.min_lr,
                                self.max_lr).decompose


class GD:

    """
    **Gradient Descent (GD)**

    GD optimizes parameters theta of an objective function J(theta) by  updating
    all of the  training samples in the  dataset. The update is perfomed in  the
    opposite  direction of  the  gradient of the  objective  function  d/d_theta
    J(theta) - with respect  to  the parameters (theta).  The learning rate  eta
    helps determine the size of teh steps we take to the minima

    References:
        [1] An overview of gradient descent optimization algorithms
            * [Sebastien Ruder, 2016] https://arxiv.org/abs/1609.04747
            * [PDF] https://arxiv.org/pdf/1609.04747.pdf
    """

    def __init__(self): pass


class SGD(Optimizer):

    """
    **Stochastic Gradient Descent (SGD)**

    SGD optimizes parameters theta of an objective function J(theta) by updating
    each of the training samples inputs(i) and targets(i) for all samples in the
    dataset. The update is perfomed in the opposite direction of the gradient of
    the objective function d/d_theta J(theta) - with respect  to the  parameters
    (theta). The learning rate eta helps determine the size of the steps we take
    to the minima

    References:
        [1] An overview of gradient descent optimization algorithms
            * [Sebastien Ruder, 2016] https://arxiv.org/abs/1609.04747
            * [PDF] https://arxiv.org/pdf/1609.04747.pdf

        [2] Large-Scale Machine Learning with Stochastic Gradient Descent
            * [Leon Botou, 2011][PDF] http://leon.bottou.org/publications/pdf/compstat-2010.pdf

    Args:
        kwargs: Arbitrary keyword arguments.
    """

    def __init__(self, **kwargs):
        super(SGD, self).__init__(**kwargs)
        self.lr = kwargs['lr'] if 'lr' in kwargs else 0.01

    def update(self, weights, grads, epoch_num, batch_num, batch_size):
        self.weights = weights
        self.grads   = grads

        self.weights -= np.multiply(super(SGD, self).get_learning_rate(epoch_num), self.grads, dtype = np.float128)

        return self.weights

    @property
    def optimization_name(self):
        return self.__class__.__name__


class SGDMomentum(Optimizer):

    """
    **Stochastic Gradient Descent with Momentum (SGDMomentum)**

    The objective function  regularly forms  places on  the contour map in which
    the surface  curves more steeply  than  others (ravines). Standard SGD  will
    tend to  oscillate across the  narrow  ravine since  the  negative  gradient
    will  point  down one  of  the  steep  sides  rather than  along the  ravine
    towards  the  optimum.  Momentum  hepls to  push the  objective more quickly
    along the shallow ravine towards the global minima

    References:
        [1] An overview of gradient descent optimization algorithms
            * [Sebastien Ruder, 2016] https://arxiv.org/abs/1609.04747
            * [PDF] https://arxiv.org/pdf/1609.04747.pdf

        [2] On the Momentum Term in Gradient Descent Learning Algorithms
            * [Ning Qian, 199] https://goo.gl/7fhr14
            * [PDF] https://goo.gl/91HtDt

        [3] Two problems with backpropagation and other steepest-descent learning procedures for networks.
            * [Sutton, R. S., 1986][PDF] https://goo.gl/M3VFM1

    Args:
        kwargs: Arbitrary keyword arguments.
    """

    def __init__(self, **kwargs):
        super(SGDMomentum, self).__init__(**kwargs)
        self.lr       = kwargs['lr']       if 'lr'       in kwargs else 0.01
        self.momentum = kwargs['momentum'] if 'momemtum' in kwargs else 0.1
        self.velocity = None

    def update(self, weights, grads, epoch_num, batch_num, batch_size):
        self.weights = weights
        self.grads   = grads

        if self.velocity is None:
            self.velocity = np.zeros_like(self.weights)

        self.velocity  = np.subtract(
                            np.multiply(self.momentum, self.velocity),
                            np.multiply(super(SGDMomentum, self).get_learning_rate(epoch_num), self.grads)
                         )
        self.weights  += self.velocity

        return self.weights

    @property
    def optimization_name(self):
        return self.__class__.__name__


class Adam(Optimizer):

    """
    **Adaptive Moment Estimation (Adam)**

    Adam computes adaptive  learning rates for by  updating each of the training
    samples while storing  an  exponentially  decaying  average of past  squared
    gradients. Adam  also  keeps  an  exponentially  decaying  average  of  past
    gradients.

    References:
        [1] An overview of gradient descent optimization algorithms
            * [Sebastien Ruder, 2016] https://arxiv.org/abs/1609.04747
            * [PDF] https://arxiv.org/pdf/1609.04747.pdf

        [2] Adam: A Method for Stochastic Optimization
            * [Diederik P. Kingma et. al., 2014] https://arxiv.org/abs/1412.6980
            * [PDF] https://arxiv.org/pdf/1412.6980.pdf

    Args:
        kwargs: Arbitrary keyword arguments.
    """

    def __init__(self, **kwargs):
        super(Adam, self).__init__(**kwargs)
        self.lr      = kwargs['lr']      if 'lr'      in kwargs else 0.001
        self.epsilon = kwargs['epsilon'] if 'epsilon' in kwargs else 1e-8
        self.beta1   = kwargs['beta1']   if 'beta1'   in kwargs else 0.9
        self.beta2   = kwargs['beta2']   if 'beta2'   in kwargs else 0.999
        self.m       = None
        self.v       = None
        self.t       = 1

    def update(self, weights, grads, epoch_num, batch_num, batch_size):
        self.weights = weights
        self.grads   = grads
        self.t       = batch_num

        if self.m is None:
            self.m = np.zeros_like(self.weights)

        if self.v is None:
            self.v = np.zeros_like(self.weights)

        self.m = np.multiply(self.beta1, self.m) + np.multiply((1 - self.beta1), self.grads)
        m_hat  = np.true_divide(self.m, (1 - np.power(self.beta1, self.t)))

        self.v = np.multiply(self.beta2, self.v)  + np.multiply((1 - self.beta2), np.square(self.grads))
        v_hat  = np.true_divide(self.v, (1 - np.power(self.beta2, self.t)))

        self.weights -= np.true_divide(
                           np.multiply(super(Adam, self).get_learning_rate(epoch_num), m_hat),
                           (np.sqrt(v_hat) + self.epsilon)
                        )

        return self.weights

    @property
    def optimization_name(self):
        return self.__class__.__name__


class Adamax(Optimizer):

    """
    **Admax**

    AdaMax is a variant of Adam based on the infinity norm. The Adam update rule
    for individual weights is to scale their gradients inversely proportional to
    a (scaled) L2  norm of  their  individual c urrent and  past  gradients. For
    Adamax we generalize the L2 norm based update rule to a Lp norm based update
    rule. These variants are numerically unstable for large p.  but have special
    cases where as p tens to infinity, a simple and stable algorithm emerges.

    References:
        [1] An overview of gradient descent optimization algorithms
            * [Sebastien Ruder, 2016] https://arxiv.org/abs/1609.04747
            * [PDF] https://arxiv.org/pdf/1609.04747.pdf

        [2] Adam: A Method for Stochastic Optimization
            * [Diederik P. Kingma et. al., 2014] https://arxiv.org/abs/1412.6980
            * [PDF] https://arxiv.org/pdf/1412.6980.pdf

    Args:
        kwargs: Arbitrary keyword arguments.
    """

    def __init__(self, **kwargs):
        super(Adamax, self).__init__(**kwargs)
        self.lr      = kwargs['lr']      if 'lr'      in kwargs else 0.02
        self.epsilon = kwargs['epsilon'] if 'epsilon' in kwargs else 1e-8
        self.beta1   = kwargs['beta1']   if 'beta1'   in kwargs else 0.9
        self.beta2   = kwargs['beta2']   if 'beta2'   in kwargs else 0.999
        self.m       = None
        self.u       = None
        self.t       = 1

    def update(self, weights, grads, epoch_num, batch_num, batch_size):
        self.weights = weights
        self.grads   = np.true_divide(grads, batch_size)
        self.t       = batch_num

        if self.m is None:
            self.m = np.zeros_like(self.weights)

        if self.u is None:
            self.u = np.zeros_like(self.weights)

        lr_t = np.true_divide(super(Adamax, self).get_learning_rate(epoch_num),
                              1. - np.power(self.beta1, self.t))

        m_hat = np.multiply(self.beta1, self.m) + np.multiply((1. - self.beta1), self.grads)
        u_hat = np.maximum(np.multiply(self.beta2, self.u), np.abs(self.grads))

        self.weights -= np.true_divide(np.multiply(lr_t, m_hat), (u_hat + self.epsilon))

        return self.weights

    @property
    def optimization_name(self):
        return self.__class__.__name__


class AdaGrad(Optimizer):

    """
    **Adaptive Gradient Algorithm (AdaGrad)**

    AdaGrad is an  optimization method  that  allows  different  step  sizes for
    different  features.  It increases  the  influence of  rare  but informative
    features

    References:
        [1] An overview of gradient descent optimization algorithms
            * [Sebastien Ruder, 2016] https://arxiv.org/abs/1609.04747
            * [PDF] https://arxiv.org/pdf/1609.04747.pdf

        [2] Adaptive Subgradient Methods for Online Learning and Stochastic Optimization
            * [John Duchi et. al., 2011] http://jmlr.org/papers/v12/duchi11a.html
            * [PDF] http://www.jmlr.org/papers/volume12/duchi11a/duchi11a.pdf

    Args:
        kwargs: Arbitrary keyword arguments.
    """

    def __init__(self, **kwargs):
        super(AdaGrad, self).__init__(**kwargs)
        self.lr      = kwargs['lr']      if 'lr'      in kwargs else 0.01
        self.epsilon = kwargs['epsilon'] if 'epsilon' in kwargs else 1e-8
        self.cache   = None

    def update(self, weights, grads, epoch_num, batch_num, batch_size):
        self.weights = weights
        self.grads   = np.true_divide(grads, batch_size)

        if self.cache is None:
            self.cache = np.zeros_like(self.grads)

        self.cache   += np.square(self.grads)
        self.weights -= np.multiply(
                            super(AdaGrad, self).get_learning_rate(epoch_num),
                            np.true_divide(self.grads, np.sqrt(self.cache) + self.epsilon)
                        )

        return self.weights

    @property
    def optimization_name(self):
        return self.__class__.__name__


class Adadelta(Optimizer):

    """
    **An Adaptive Learning Rate Method (Adadelta)**

    Adadelta is an extension of Adagrad that seeks to avoid setting  the learing
    rate to an aggresively  monotonically  decreasing rate. This is achieved via
    a dynamic learning rate i.e a diffrent learning  rate is computed  for  each
    training sample

    References:
        [1] An overview of gradient descent optimization algorithms
            * [Sebastien Ruder, 2016] https://arxiv.org/abs/1609.04747
            * [PDF] https://arxiv.org/pdf/1609.04747.pdf

        [2] ADADELTA: An Adaptive Learning Rate Method
            * [Matthew D. Zeiler, 2012] https://arxiv.org/abs/1212.5701
            * [PDF] https://arxiv.org/pdf/1212.5701.pdf

    Args:
        kwargs: Arbitrary keyword arguments.
    """

    def __init__(self, **kwargs):
        super(Adadelta, self).__init__(**kwargs)
        self.lr      = kwargs['lr']      if 'lr'      in kwargs else 1.0
        self.epsilon = kwargs['epsilon'] if 'epsilon' in kwargs else 1e-6
        self.rho     = kwargs['rho']     if 'rho'     in kwargs else 0.9
        self.cache   = None
        self.delta   = None

    def update(self, weights, grads, epoch_num, batch_num, batch_size):
        self.weights = weights
        self.grads   = np.true_divide(grads, batch_size) # grads

        if self.cache is None:
            self.cache = np.zeros_like(self.weights)

        if self.delta is None:
            self.delta = np.zeros_like(self.weights)

        self.cache = np.multiply(self.rho, self.cache) + np.multiply(1 - self.rho, np.square(self.grads))

        RMSE_grad  = np.sqrt(self.cache + self.epsilon)
        RMSE_delta = np.sqrt(self.delta + self.epsilon)

        update = np.multiply(self.grads, np.true_divide(RMSE_delta, RMSE_grad))

        self.weights -= np.multiply(super(Adadelta, self).get_learning_rate(epoch_num), update)
        self.delta    = np.multiply(self.rho, self.delta) + np.multiply((1 - self.rho), np.square(update))

        return self.weights

    @property
    def optimization_name(self):
        return self.__class__.__name__


class RMSprop(Optimizer):

    """
    **Root Mean Squared Propagation (RMSprop)**

    RMSprop utilizes  the magnitude of recent gradients to  normalize  gradients.
    A moving average over the root mean squared (RMS) gradients is kept and then
    divided by  the current  gradient. Parameters are  recomended to  be  set as
    follows rho = 0.9 and eta (learning rate) = 0.001

    References:
        [1] An overview of gradient descent optimization algorithms
            * [Sebastien Ruder, 2016] https://arxiv.org/abs/1609.04747
            * [PDF] https://arxiv.org/pdf/1609.04747.pdf

        [2] Lecture 6.5 - rmsprop, COURSERA: Neural Networks for Machine Learning
            * [Tieleman, T. and Hinton, G. 2012][PDF] https://goo.gl/Dhkvpk

    Args:
        kwargs: Arbitrary keyword arguments.
    """

    def __init__(self, **kwargs):
        super(RMSprop, self).__init__(**kwargs)
        self.lr      = kwargs['lr']      if 'lr'      in kwargs else 0.001
        self.epsilon = kwargs['epsilon'] if 'epsilon' in kwargs else 1e-6
        self.rho     = kwargs['rho']     if 'rho'     in kwargs else 0.9
        self.cache   = None

    def update(self, weights, grads, epoch_num, batch_num, batch_size):
        self.weights = weights
        self.grads   = np.true_divide(grads, batch_size) # grads

        if self.cache is None:
            self.cache = np.zeros_like(self.weights)

        self.cache    = np.multiply(self.rho, np.multiply(self.cache + (1 - self.rho), np.square(self.grads)))
        self.weights -= np.multiply(self.lr, np.true_divide(self.grads, (np.sqrt(self.cache) + self.epsilon)))

        return self.weights

    @property
    def optimization_name(self):
        return self.__class__.__name__


class NesterovAcceleratedGradient(Optimizer):

    """
    **Nesterov Accelerated Gradient (NAG)**

    NAG is an improvement in SGDMomentum where the the previous parameter values
    are smoothed and a gradient  descent  step is taken from this smoothed value.
    This enables a more intelligent way of arriving at the minima

    References:
        [1] An overview of gradient descent optimization algorithms
            * [Sebastien Ruder, 2016] https://arxiv.org/abs/1609.04747
            * [PDF] https://arxiv.org/pdf/1609.04747.pdf

        [2] A method for unconstrained convex minimization problem with the rate of convergence
            * [Nesterov, Y. 1983][PDF] https://goo.gl/X8313t

        [3] Nesterov's Accelerated Gradient and Momentum as approximations to Regularised Update Descent
            * [Aleksandar Botev, 2016] https://arxiv.org/abs/1607.01981
            * [PDF] https://arxiv.org/pdf/1607.01981.pdf

    Args:
        kwargs: Arbitrary keyword arguments.
    """

    def __init__(self, **kwargs):
        super(NesterovAcceleratedGradient, self).__init__(**kwargs)
        self.lr            = kwargs['lr']       if 'lr'       in kwargs else 0.001
        self.momentum      = kwargs['momentum'] if 'momemtum' in kwargs else 0.9
        self.velocity_prev = None
        self.velocity      = None

    def update(self, weights, grads, epoch_num, batch_num, batch_size):
        self.weights = weights
        self.grads   = grads

        if self.velocity_prev is None:
            self.velocity_prev = np.zeros_like(self.weights)

        if self.velocity is None:
            self.velocity = np.zeros_like(self.weights)

        self.velocity_prev  = self.velocity
        self.velocity       = np.subtract(
                                 np.multiply(self.momentum, self.velocity),
                                 np.multiply(super(NesterovAcceleratedGradient, self).get_learning_rate(epoch_num), self.grads)
                              )
        self.weights       += np.multiply(-self.momentum, self.velocity_prev) + np.multiply(1 + self.momentum, self.velocity)

        return self.weights

    @property
    def optimization_name(self):
        return self.__class__.__name__


class OptimizationFunction:

    _optimizers = {
        'sgd'          : SGD,
        'adam'         : Adam,
        'adamax'       : Adamax,
        'adagrad'      : AdaGrad,
        'rmsprop'      : RMSprop,
        'adadelta'     : Adadelta,
        'sgd_momentum' : SGDMomentum,
        'nestrov'      : NesterovAcceleratedGradient
    }

    def __init__(self, optimizer_kwargs):

        # 1. using class types: check if optimizer_kwargs is an instance of any of the classes in _optimizers.values dict
        if any(isinstance(optimizer_kwargs, cls_type) for cls_type in list(self._optimizers.values())):
            import copy
            self.optimization_func = copy.copy(optimizer_kwargs)

        # 2. using string types: check if optimizer_kwargs is an instance of any of type string and is in _optimizers.keys dict
        elif any(isinstance(optimizer_kwargs, str) for cls_type in list(self._optimizers.keys())):
            if optimizer_kwargs not in self._optimizers.keys():
                raise Exception('Optimization function must be either one of the following: {}.'.format(', '.join(self._optimizers.keys())))
            self.optimization_func = self._optimizers[optimizer_kwargs]()

        # 3. using kwargs: we have a dictionary of keyword arguments from the register_opt func
        else:
            if optimizer_kwargs['optimizer_name'] not in self._optimizers.keys():
                raise Exception('Optimization function must be either one of the following: {}.'.format(', '.join(self._optimizers.keys())))
            self.optimization_func = self._optimizers[optimizer_kwargs['optimizer_name']](**optimizer_kwargs)

    @property
    def name(self):
        return self.optimization_func.optimization_name

    def update(self, weights, grads, epoch_num, batch_num, batch_size):
        return self.optimization_func.update(weights, grads, epoch_num, batch_num, batch_size)


def register_opt(**kwargs):

    # ensure that key optimizer_name is present
    if 'optimizer_name' not in kwargs:
        raise Exception('optimizer_name must be included in the register_opt func to deduce the optimization type to be used')

    allowed_kwargs = {
        'lr',
        'rho',
        'beta2',
        'beta1',
        'epsilon',
        'epsilon',
        'decay_lr',
        'momentum',
        'velocity',
        'step_size',
        'decay_rate',
        'decay_func',
        'optimizer_name'
    }

    for kwrd in kwargs:
        if kwrd not in allowed_kwargs:
            raise TypeError('Unexpected keyword argument passed to optimizer: ' + str(kwrd))
    return kwargs
