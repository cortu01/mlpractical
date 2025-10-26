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

    def __repr__(self):
        return 'SingleLayerModel(' + str(layer) + ')'


class MultipleLayerModel(object):
    """A model consisting of multiple layers applied sequentially."""

    def __init__(self, layers):
        """Create a new multiple layer model instance.

        Args:
            layers: List of the the layer objecst defining the model in the
                order they should be applied from inputs to outputs.
        """
        self.layers = layers

    @property
    def params(self):
        """A list of all of the parameters of the model."""
        params = []
        for layer in self.layers:
            if isinstance(layer, LayerWithParameters):
                params += layer.params
        return params

    def fprop(self, inputs):
        """Forward propagates a batch of inputs through the model.

        Args:
            inputs: Batch of inputs to the model.

        Returns:
            List of the activations at the output of all layers of the model
            plus the inputs (to the first layer) as the first element. The
            last element of the list corresponds to the model outputs.
        """
        activations = [inputs]
        for i, layer in enumerate(self.layers):
            activations.append(self.layers[i].fprop(activations[i]))
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
        grads_wrt_params = []
        for i, layer in enumerate(self.layers[::-1]):
            inputs = activations[-i - 2]
            outputs = activations[-i - 1]
            grads_wrt_inputs = layer.bprop(inputs, outputs, grads_wrt_outputs)
            if isinstance(layer, LayerWithParameters):
                grads_wrt_params += layer.grads_wrt_params(
                    inputs, grads_wrt_outputs)[::-1]
            grads_wrt_outputs = grads_wrt_inputs
        return grads_wrt_params[::-1]

    def __repr__(self):
        return (
            'MultiLayerModel(\n    ' +
            '\n    '.join([str(layer) for layer in self.layers]) +
            '\n)'
        )
