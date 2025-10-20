# -*- coding: utf-8 -*-
"""Training schedulers.

This module contains classes implementing schedulers which control the
evolution of learning rule hyperparameters (such as learning rate) over a
training run.
"""

import numpy as np


class ConstantLearningRateScheduler(object):
    """Example of scheduler interface which sets a constant learning rate."""

    def __init__(self, learning_rate):
        """Construct a new constant learning rate scheduler object.

        Args:
            learning_rate: Learning rate to use in learning rule.
        """
        self.learning_rate = learning_rate

    def update_learning_rule(self, learning_rule, epoch_number):
        """Update the hyperparameters of the learning rule.

        Run at the beginning of each epoch.

        Args:
            learning_rule: Learning rule object being used in training run,
                any scheduled hyperparameters to be altered should be
                attributes of this object.
            epoch_number: Integer index of training epoch about to be run.
        """
        learning_rule.learning_rate = self.learning_rate
