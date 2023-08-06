"""
.. module:: CNormalizerMeanStd
   :synopsis: Scales input array features using specific mean and variance.

.. moduleauthor:: Marco Melis <marco.melis@unica.it>
.. moduleauthor:: Battista Biggio <battista.biggio@unica.it>

"""
from __future__ import division
from six.moves import range

from secml.array import CArray
from secml.core.type_utils import is_scalar
from secml.core.decorators import deprecated
from secml.ml.features.normalization import CNormalizerLinear


class CNormalizerMeanStd(CNormalizerLinear):
    """Normalize with given mean and standard deviation.

    If mean/std are tuples of multiple values, input is expected to be
    uniformly splittable in a number of channels equal to the number of
    values in the tuples. Both input tuples must have the same length.

    Result will be: (input[channel] - mean[channel]) / std[channel]

    If mean and std are None, values to use as mean and std will be computed
    from data. The result wil be an array with 0 mean or/and unit variance
    (if with_std parameter is True, default). In this case, the standard
    deviation calculated by numpy is the maximum likelihood estimate,
    i.e. the second moment of the set of values about their mean.
    See also :meth:`.CArray.std` for more information.

    Parameters
    ----------
    mean : scalar or tuple of scalars or None, optional
        Mean to use for normalization. If a tuple, each value represent
        a channel of the input. The number of features of the training data
        should be divisible by the number of values of the tuple.
        If a scalar, the same value is applied to all features.
        If None, mean is computed from training data.
        Cannot be None if `std` is not None and `with_std` is True.
    std : scalar or tuple of scalars or None, optional
        Variance to use for normalization. If a tuple, each value represent
        a channel of the input. The number of features of the training data
        should be divisible by the number of values of the tuple.
        If a scalar, the same value is applied to all features.
        If None, std is computed from training data.
        Cannot be None if `mean` is not None and `with_std` is True.
    with_std : bool, optional
        If True (default), normalizer scales array using std too.
        If False, `std` parameter is ignored.
    preprocess : CPreProcess or str or None, optional
        Features preprocess to be applied to input data.
        Can be a CPreProcess subclass or a string with the type of the
        desired preprocessor. If None, input data is used as is.

    Attributes
    ----------
    class_type : 'mean-std'

    """
    __class_type = 'mean-std'

    def __init__(self, mean=None, std=None, with_std=True, preprocess=None):

        if mean is not None:
            self._mean = (mean,) if is_scalar(mean) else tuple(mean)
        else:  # mean is None
            self._mean = None
        if std is not None:
            self._std = (std,) if is_scalar(std) else tuple(std)
        else:  # std is None
            self._std = None

        # Input validation
        if with_std is True:
            if (mean is None and std is not None) or \
                    (mean is not None and std is None) or \
                    (mean is not None and std is not None and
                     len(self._mean) != len(self._std)):
                raise ValueError("if `with_std` is True, `mean` and `std` "
                                 "should be both None or both scalar or "
                                 "both tuple of the same length")

        self._x_mean = None
        self._x_std = None

        self._with_std = with_std

        # Properties of the linear normalizer
        self._w = None
        self._b = None

        super(CNormalizerMeanStd, self).__init__(preprocess=preprocess)

    @property
    def w(self):
        """Returns the slope of the linear normalizer."""
        return self._w

    @property
    def b(self):
        """Returns the bias of the linear normalizer."""
        return self._b

    @property
    def mean(self):
        """Mean to use for normalization.

        One value for each training array feature.

        """
        return self._x_mean

    @property
    def std(self):
        """Variance to use for normalization.

        One value for each training array feature.

        """
        return self._x_std

    @property
    def with_std(self):
        """True if normalizer should transform array using variance too."""
        return self._with_std

    def _expand_mean(self, n_feats):
        """Expand mean value to all dimensions."""
        n_channels = len(self._mean)
        if not n_feats % n_channels == 0:
            raise ValueError("input number of features must be "
                             "divisible by {:}".format(n_channels))
        channel_size = int(n_feats / n_channels)
        self._x_mean = CArray.ones(shape=(n_feats,))
        for i in range(n_channels):
            self._x_mean[i * channel_size:
                         i * channel_size + channel_size] *= self._mean[i]
        return self._x_mean

    def _expand_std(self, n_feats):
        """Expand std value to all dimensions."""
        if self.with_std is False:
            # set std to 1.
            self._x_std = CArray(1.0)  # we just need a scalar value.
        else:
            n_channels = len(self._std)
            if not n_feats % n_channels == 0:
                raise ValueError("input number of features must be "
                                 "divisible by {:}".format(n_channels))
            channel_size = int(n_feats / n_channels)
            self._x_std = CArray.ones(shape=(n_feats,))
            for i in range(n_channels):
                self._x_std[i * channel_size:
                            i * channel_size + channel_size] *= self._std[i]
        return self._x_std

    def _compute_w_and_b(self):
        # Updating linear normalizer parameters
        self._w = CArray.ones(self._x_mean.size)  # TODO: this can be scalar!
        self._b = -self._x_mean

        # Makes sure that whenever scale is zero, we handle it correctly
        scale = self.std.deepcopy()
        scale[scale == 0.0] = 1.0

        # Updating linear normalizer parameters
        self._w /= scale
        self._b /= scale

    def _fit(self, x, y=None):
        """Compute the mean and standard deviation to be used for scaling.

        Parameters
        ----------
        x : CArray
            Array to be used as training set. Each row must correspond to
            one single patterns, so each column is a different feature.
        y : CArray or None, optional
            Flat array with the label of each pattern.
            Can be None if not required by the preprocessing algorithm.

        Returns
        -------
        CNormalizerMeanStd
            Instance of the trained normalizer.

        Examples
        --------
        >>> from secml.array import CArray
        >>> from secml.ml.features.normalization import CNormalizerMeanStd
        >>> array = CArray([[1., -1., 2.], [2., 0., 0.], [0., 1., -1.]],tosparse=True)

        >>> normalizer = CNormalizerMeanStd(0.5, 0.2).fit(array)
        >>> print(normalizer.mean)
        CArray([0.5 0.5 0.5])
        >>> print(normalizer.std)
        CArray([0.2 0.2 0.2])

        >>> print(normalizer.transform(array))
        CArray([[ 2.5 -7.5  7.5]
         [ 7.5 -2.5 -2.5]
         [-2.5  2.5 -7.5]])

        >>> normalizer = CNormalizerMeanStd((0.5, 0.5, 0.2), (0.2, 0.1, 0.1)).fit(array)

        >>> print(normalizer.transform(array))
        CArray([[  2.5 -15.   18. ]
         [  7.5  -5.   -2. ]
         [ -2.5   5.  -12. ]])

        >>> out = CNormalizerMeanStd().fit_transform(array)
        >>> # Expected zero mean and unit variance
        >>> print(out.mean(axis=0, keepdims=False))
        CArray([0. 0. 0.])
        >>> print(out.std(axis=0, keepdims=False))
        CArray([1. 1. 1.])

        """
        n_feats = x.shape[1]

        # Setting the mean
        if self._mean is None:
            # Compute values from training data
            self._x_mean = x.mean(axis=0, keepdims=False)
        else:  # Expand _mean tuple and build _x_mean
            self._x_mean = self._expand_mean(n_feats)

        # Setting the variance
        if self.with_std is False:
            # Use a "neutral" value
            self._x_std = CArray(1.0)  # we just need a scalar value.
        elif self._std is None:
            # Compute values from training data
            self._x_std = x.std(axis=0, keepdims=False)
        else:  # Expand _std tuple and build _x_std
            self._x_std = self._expand_std(n_feats)

        self._compute_w_and_b()

        return self

    def transform(self, x, caching=False):
        """Apply the transformation algorithm on data.

        Parameters
        ----------
        x : CArray
            Array to be transformed.
            Shape of input array depends on the algorithm itself.
        caching: bool
                 True if preprocessed input should be cached for backward pass.

        Returns
        -------
        CArray
            Transformed input data.

        """

        # this avoids calling fit before transform,
        # when default params are set
        n_feats = x.atleast_2d().shape[1]
        if self.w is None:
            if self._mean is not None:
                self._expand_mean(n_feats)
            if self._std is not None:
                self._expand_std(n_feats)
            self._compute_w_and_b()

        return super(CNormalizerMeanStd, self).transform(x, caching)


@deprecated('0.10', "use `CNormalizerMeanStd` instead.")
class CNormalizerMeanSTD(CNormalizerMeanStd):
    """Normalize with given mean and standard deviation."""

    def __init__(self, *args, **kwargs):

        super(CNormalizerMeanSTD, self).__init__(*args, **kwargs)
