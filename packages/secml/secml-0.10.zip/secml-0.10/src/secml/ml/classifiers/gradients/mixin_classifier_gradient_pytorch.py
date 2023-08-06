"""
.. module:: CClassifierGradientPytorchMixin
   :synopsis: Mixin for Pytorch classifier gradients.

.. moduleauthor:: Marco Melis <marco.melis@unica.it>
.. moduleauthor:: Ambra Demontis <ambra.demontis@unica.it>
.. moduleauthor:: Maura Pintor <maura.pintor@unica.it>

"""
import torch

from secml.array import CArray
from secml.ml.classifiers.gradients import CClassifierGradientDNNMixin
from secml.ml.classifiers.loss import CSoftmax

from secml.settings import SECML_PYTORCH_USE_CUDA

use_cuda = torch.cuda.is_available() and SECML_PYTORCH_USE_CUDA


class CClassifierGradientPyTorchMixin(CClassifierGradientDNNMixin):
    """Mixin class for CClassifierPyTorch gradients."""

    def _grad_f_x(self, x, y=None, w=None, layer=None):
        """Computes the gradient of the classifier's decision function
         wrt input.

        Parameters
        ----------
        x : CArray
            The gradient is computed in the neighborhood of x.
        y : int or None, optional
            Index of the class wrt the gradient must be computed.
            This is not required if:
             - `w` is passed and the last layer is used but
              softmax_outputs is False
             - an intermediate layer is used
        w : CArray or None, optional
            If CArray, will be passed to backward and must have a proper shape
            depending on the chosen output layer (the last one if `layer`
            is None). This is required if `layer` is not None.
        layer : str or None, optional
            Name of the layer.
            If None, the gradient at the last layer will be returned
             and `y` is required if `w` is None or softmax_outputs is True.
            If not None, `w` of proper shape is required.

        Returns
        -------
        gradient : CArray
            Gradient of the classifier's df wrt its input. Vector-like array.

        """
        if x.is_vector_like is False:
            raise ValueError("gradient can be computed on one sample only.")
        if isinstance(layer, list):
            raise ValueError("gradient can be computed on one layer at a time.")

        # Transform data if a preprocess is defined
        s, _ = next(iter(self._data_loader(x)))

        if use_cuda is True:
            s = s.cuda()

        # keep track of the gradient in s tensor
        s.requires_grad = True

        # Get the model output at specific layer
        layer_output = self._get_layer_output(s, layer_names=layer)
        if isinstance(layer_output, dict):
            layer_output = layer_output[layer]

        if w is not None and y is None:
            w = self._to_tensor(w.atleast_2d()).reshape(layer_output.shape)
        elif y is not None and w is None and layer is None:
            w = torch.zeros(layer_output.shape)
            w[0, y] = 1
            w = w.to(self._device)

            # Apply softmax-scaling if needed
            if self.softmax_outputs is True:
                out_carray = self._from_tensor(layer_output.squeeze(0).data)
                softmax_grad = CSoftmax().gradient(out_carray, y=y)
                layer_output *= self._to_tensor(softmax_grad.atleast_2d()).unsqueeze(0)
        else:
            # both `w` and `y` are passed or none of them
            raise ValueError("Either `w` or `y` must be passed.")

        w = w.to(self._device)

        if s.grad is not None:
            s.grad.data._zero()

        layer_output.backward(w)

        return self._from_tensor(s.grad.data.view(-1))
