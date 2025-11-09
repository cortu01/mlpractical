import numpy as np

seed = 22102017
rng = np.random.RandomState(seed)


class L1Penalty(object):
    """L1 parameter penalty.

    Term to add to the objective function penalising parameters
    based on their L1 norm.
    """

    def __init__(self, coefficient):
        """Create a new L1 penalty object.

        Args:
            coefficient: Positive constant to scale penalty term by.
        """
        assert coefficient > 0., 'Penalty coefficient must be positive.'
        self.coefficient = coefficient

    def __call__(self, parameter):
        """Calculate L1 penalty value for a parameter.

        Args:
            parameter: Array corresponding to a model parameter.

        Returns:
            Value of penalty term.
        """
        return self.coefficient * np.sum(np.abs(parameter))

    def grad(self, parameter):
        """Calculate the penalty gradient with respect to the parameter.

        Args:
            parameter: Array corresponding to a model parameter.

        Returns:
            Value of penalty gradient with respect to parameter. This
            should be an array of the same shape as the parameter.
        """
        g = np.sign(parameter)
        g[parameter == 0] = 0.0
        return self.coefficient * g

    def __repr__(self):
        return 'L1Penalty({0})'.format(self.coefficient)


class L2Penalty(object):
    """L1 parameter penalty.

    Term to add to the objective function penalising parameters
    based on their L2 norm.
    """

    def __init__(self, coefficient):
        """Create a new L2 penalty object.

        Args:
            coefficient: Positive constant to scale penalty term by.
        """
        assert coefficient > 0., 'Penalty coefficient must be positive.'
        self.coefficient = coefficient

    def __call__(self, parameter):
        """Calculate L2 penalty value for a parameter.

        Args:
            parameter: Array corresponding to a model parameter.

        Returns:
            Value of penalty term.
        """
        return 0.5 * self.coefficient * np.sum(parameter ** 2)
    
    def grad(self, parameter):
        """Calculate the penalty gradient with respect to the parameter.

        Args:
            parameter: Array corresponding to a model parameter.

        Returns:
            Value of penalty gradient with respect to parameter. This
            should be an array of the same shape as the parameter.
        """
        return self.coefficient * parameter

    def __repr__(self):
        return 'L2Penalty({0})'.format(self.coefficient)

class L1L2MixPenalty(object):
    def __init__(self, coefficient, l1_ratio=0.5):
        assert coefficient > 0., 'Penalty coefficient must be positive.'
        assert 0.0 <= l1_ratio <= 1.0, 'l1_ratio in [0,1].'
        self.coefficient = coefficient
        self.l1_ratio = l1_ratio

    def __call__(self, parameter):
        # λ [ ρ * ||w||_1 + (1-ρ) * 1/2 * ||w||_2^2 ]
        l1 = np.abs(parameter).sum()
        l2 = 0.5 * np.square(parameter).sum()
        return self.coefficient * (self.l1_ratio * l1 + (1. - self.l1_ratio) * l2)

    def grad(self, parameter):
        # λ [ ρ * sign(w) + (1-ρ) * w ]
        sign = np.sign(parameter)
        sign[parameter == 0] = 0.0  # 次梯度取0
        return self.coefficient * (self.l1_ratio * sign + (1. - self.l1_ratio) * parameter)

    def __repr__(self):
        return 'L1L2MixPenalty({0})'.format(self.coefficient)
