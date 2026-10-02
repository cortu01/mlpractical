# -*- coding: utf-8 -*-
"""Model definitions.

This module implements objects encapsulating learnable models of input-output
relationships. The model objects implement methods for forward propagating
the inputs through the transformation(s) defined by the model to produce
outputs (and intermediate states) and for calculating gradients of scalar
functions of the outputs with respect to the model parameters.
"""

from mlp.layers import LayerWithParameters


class SingleLayerModel(object):
    """A model consisting of a single transformation layer."""

    def __init__(self, layer):
        """Create a new single layer model instance.

        Args:
            layer: The layer object defining the model architecture.
        """
        self.layer = layer

    @property
    def params(self):
        """A list of all of the parameters of the model."""
        return self.layer.params

    def fprop(self, inputs):
        """Calculate the model outputs corresponding to a batch of inputs.

        Args:
            inputs: Batch of inputs to the model.

        Returns:
            List which is a concatenation of the model inputs and model
            outputs, this being done for consistency of the interface with
            multi-layer models for which `fprop` returns a list of
            activations through all immediate layers of the model and including
            the inputs and outputs.
        """
        activations = [inputs, self.layer.fprop(inputs)]
        return activations

    def grads_wrt_params(self, activations, grads_wrt_outputs):
        """Calculates gradients with respect to the model parameters.

        Args:
            activations: List of all activations from forward pass through
                model using `fprop`.
            grads_wrt_outputs: Gradient with respect to the model outputs of
               the scalar function parameter gradients are being calculated
               for.

        Returns:
            List of gradients of the scalar function with respect to all model
            parameters.
        """
        return self.layer.grads_wrt_params(activations[0], grads_wrt_outputs)

    def params_cost(self):
        """Calculates the parameter dependent cost term of the model."""
        return self.layer.params_cost()

    def __repr__(self):
        return 'SingleLayerModel(' + str(self.layer) + ')'
