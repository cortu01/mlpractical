# -*- coding: utf-8 -*-
"""Learning rules.

This module contains classes implementing gradient based learning rules.
"""

import numpy as np


class GradientDescentLearningRule(object):
    """Simple (stochastic) gradient descent learning rule.

    For a scalar error function `E(p[0], p_[1] ... )` of some set of
    potentially multidimensional parameters this attempts to find a local
    minimum of the loss function by applying updates to each parameter of the
    form

        p[i] := p[i] - learning_rate * dE/dp[i]

    With `learning_rate` a positive scaling parameter.

    The error function used in successive applications of these updates may be
    a stochastic estimator of the true error function (e.g. when the error with
    respect to only a subset of data-points is calculated) in which case this
    will correspond to a stochastic gradient descent learning rule.
    """

    def __init__(self, learning_rate=1e-3):
        """Creates a new learning rule object.

        Args:
            learning_rate: A postive scalar to scale gradient updates to the
                parameters by. This needs to be carefully set - if too large
                the learning dynamic will be unstable and may diverge, while
                if set too small learning will proceed very slowly.

        """
        assert learning_rate > 0., 'learning_rate should be positive.'
        self.learning_rate = learning_rate

    def initialise(self, params):
        """Initialises the state of the learning rule for a set or parameters.

        This must be called before `update_params` is first called.

        Args:
            params: A list of the parameters to be optimised. Note these will
                be updated *in-place* to avoid reallocating arrays on each
                update.
        """
        self.params = params

    def reset(self):
        """Resets any additional state variables to their intial values.

        For this learning rule there are no additional state variables so we
        do nothing here.
        """
        pass

    def update_params(self, grads_wrt_params):
        """Applies a single gradient descent update to all parameters.

        All parameter updates are performed using in-place operations and so
        nothing is returned.

        Args:
            grads_wrt_params: A list of gradients of the scalar loss function
                with respect to each of the parameters passed to `initialise`
                previously, with this list expected to be in the same order.
        """
        for param, grad in zip(self.params, grads_wrt_params):
            param -= self.learning_rate * grad


class MomentumLearningRule(GradientDescentLearningRule):
    """Gradient descent with momentum learning rule.

    This extends the basic gradient learning rule by introducing extra
    momentum state variables for each parameter. These can help the learning
    dynamic help overcome shallow local minima and speed convergence when
    making multiple successive steps in a similar direction in parameter space.

    For parameter p[i] and corresponding momentum m[i] the updates for a
    scalar loss function `L` are of the form

        m[i] := mom_coeff * m[i] - learning_rate * dL/dp[i]
        p[i] := p[i] + m[i]

    with `learning_rate` a positive scaling parameter for the gradient updates
    and `mom_coeff` a value in [0, 1] that determines how much 'friction' there
    is the system and so how quickly previous momentum contributions decay.
    """

    def __init__(self, learning_rate=1e-3, mom_coeff=0.9):
        """Creates a new learning rule object.

        Args:
            learning_rate: A postive scalar to scale gradient updates to the
                parameters by. This needs to be carefully set - if too large
                the learning dynamic will be unstable and may diverge, while
                if set too small learning will proceed very slowly.
            mom_coeff: A scalar in the range [0, 1] inclusive. This determines
                the contribution of the previous momentum value to the value
                after each update. If equal to 0 the momentum is set to exactly
                the negative scaled gradient each update and so this rule
                collapses to standard gradient descent. If equal to 1 the
                momentum will just be decremented by the scaled gradient at
                each update. This is equivalent to simulating the dynamic in
                a frictionless system. Due to energy conservation the loss
                of 'potential energy' as the dynamics moves down the loss
                function surface will lead to an increasingly large 'kinetic
                energy' and so speed, meaning the updates will become
                increasingly large, potentially unstably so. Typically a value
                less than but close to 1 will avoid these issues and cause the
                dynamic to converge to a local minima where the gradients are
                by definition zero.
        """
        super(MomentumLearningRule, self).__init__(learning_rate)
        assert mom_coeff >= 0. and mom_coeff <= 1., (
            'mom_coeff should be in the range [0, 1].'
        )
        self.mom_coeff = mom_coeff

    def initialise(self, params):
        """Initialises the state of the learning rule for a set or parameters.

        This must be called before `update_params` is first called.

        Args:
            params: A list of the parameters to be optimised. Note these will
                be updated *in-place* to avoid reallocating arrays on each
                update.
        """
        super(MomentumLearningRule, self).initialise(params)
        self.moms = []
        for param in self.params:
            self.moms.append(np.zeros_like(param))

    def reset(self):
        """Resets any additional state variables to their intial values.

        For this learning rule this corresponds to zeroing all the momenta.
        """
        for mom in zip(self.moms):
            mom *= 0.

    def update_params(self, grads_wrt_params):
        """Applies a single update to all parameters.

        All parameter updates are performed using in-place operations and so
        nothing is returned.

        Args:
            grads_wrt_params: A list of gradients of the scalar loss function
                with respect to each of the parameters passed to `initialise`
                previously, with this list expected to be in the same order.
        """
        for param, mom, grad in zip(self.params, self.moms, grads_wrt_params):
            mom *= self.mom_coeff
            mom -= self.learning_rate * grad
            param += mom
            
            
class AdamLearningRule(GradientDescentLearningRule):
    """Adaptive moments (Adam) learning rule.
    First-order gradient-descent based learning rule which uses adaptive
    estimates of first and second moments of the parameter gradients to
    calculate the parameter updates.
    References:
      [1]: Adam: a method for stochastic optimisation
           Kingma and Ba, 2015
    """

    def __init__(self, learning_rate=1e-3, beta_1=0.9, beta_2=0.999,
                 epsilon=1e-8):
        """Creates a new learning rule object.
        Args:
            learning_rate: A postive scalar to scale gradient updates to the
                parameters by. This needs to be carefully set - if too large
                the learning dynamic will be unstable and may diverge, while
                if set too small learning will proceed very slowly.
            beta_1: Exponential decay rate for gradient first moment estimates.
                This should be a scalar value in [0, 1]. The running gradient
                first moment estimate is calculated using
                `m_1 = beta_1 * m_1_prev + (1 - beta_1) * g`
                 where `m_1_prev` is the previous estimate and `g` the current
                 parameter gradients.
            beta_2: Exponential decay rate for gradient second moment
                estimates. This should be a scalar value in [0, 1]. The run
                gradient second moment estimate is calculated using
                `m_2 = beta_2 * m_2_prev + (1 - beta_2) * g**2`
                 where `m_2_prev` is the previous estimate and `g` the current
                 parameter gradients.
            epsilon: 'Softening' parameter to stop updates diverging when
                second moment estimates are close to zero. Should be set to
                a small positive value.
        """
        super(AdamLearningRule, self).__init__(learning_rate)
        assert beta_1 >= 0. and beta_1 <= 1., 'beta_1 should be in [0, 1].'
        assert beta_2 >= 0. and beta_2 <= 1., 'beta_2 should be in [0, 2].'
        assert epsilon > 0., 'epsilon should be > 0.'
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.epsilon = epsilon

    def initialise(self, params):
        """Initialises the state of the learning rule for a set or parameters.
        This must be called before `update_params` is first called.
        Args:
            params: A list of the parameters to be optimised. Note these will
                be updated *in-place* to avoid reallocating arrays on each
                update.
        """
        super(AdamLearningRule, self).initialise(params)
        self.moms_1 = []
        for param in self.params:
            self.moms_1.append(np.zeros_like(param))
        self.moms_2 = []
        for param in self.params:
            self.moms_2.append(np.zeros_like(param))
        self.step_count = 0

    def reset(self):
        """Resets any additional state variables to their initial values.
        For this learning rule this corresponds to zeroing the estimates of
        the first and second moments of the gradients.
        """
        for mom_1, mom_2 in zip(self.moms_1, self.moms_2):
            mom_1 *= 0.
            mom_2 *= 0.
        self.step_count = 0

    def update_params(self, grads_wrt_params):
        """Applies a single update to all parameters.
        All parameter updates are performed using in-place operations and so
        nothing is returned.
        Args:
            grads_wrt_params: A list of gradients of the scalar loss function
                with respect to each of the parameters passed to `initialise`
                previously, with this list expected to be in the same order.
        """
        for param, mom_1, mom_2, grad in zip(
                self.params, self.moms_1, self.moms_2, grads_wrt_params):
            mom_1 *= self.beta_1
            mom_1 += (1. - self.beta_1) * grad
            mom_2 *= self.beta_2
            mom_2 += (1. - self.beta_2) * grad ** 2
            alpha_t = (
                    self.learning_rate *
                    (1. - self.beta_2 ** (self.step_count + 1)) ** 0.5 /
                    (1. - self.beta_1 ** (self.step_count + 1))
            )
            param -= alpha_t * mom_1 / (mom_2 ** 0.5 + self.epsilon)
        self.step_count += 1

