The multivariate normal distribution on `R^k`.

This distribution is defined by a 1-D mean `mu` and a 1-D diagonal
`diag_stdev`, representing the standard deviations.  This distribution
assumes the random variables, `(X_1,...,X_k)` are independent, thus no
non-diagonal terms of the covariance matrix are needed.

This allows for `O(k)` pdf evaluation, sampling, and storage.

#### Mathematical details

The PDF of this distribution is defined in terms of the diagonal covariance
determined by `diag_stdev`: `C_{ii} = diag_stdev[i]**2`.

```
f(x) = (2 pi)^(-k/2) |det(C)|^(-1/2) exp(-1/2 (x - mu)^T C^{-1} (x - mu))
```

#### Examples

A single multi-variate Gaussian distribution is defined by a vector of means
of length `k`, and the square roots of the (independent) random variables.

Extra leading dimensions, if provided, allow for batches.

```python
# Initialize a single 3-variate Gaussian with diagonal standard deviation.
mu = [1, 2, 3.]
diag_stdev = [4, 5, 6.]
dist = tf.contrib.distributions.MultivariateNormalDiag(mu, diag_stdev)

# Evaluate this on an observation in R^3, returning a scalar.
dist.pdf([-1, 0, 1])

# Initialize a batch of two 3-variate Gaussians.
mu = [[1, 2, 3], [11, 22, 33]]  # shape 2 x 3
diag_stdev = ...  # shape 2 x 3, positive.
dist = tf.contrib.distributions.MultivariateNormalDiag(mu, diag_stdev)

# Evaluate this on a two observations, each in R^3, returning a length two
# tensor.
x = [[-1, 0, 1], [-11, 0, 11]]  # Shape 2 x 3.
dist.pdf(x)
```
- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.__init__(mu, diag_stdev, validate_args=True, allow_nan_stats=False, name='MultivariateNormalDiag')` {#MultivariateNormalDiag.__init__}

Multivariate Normal distributions on `R^k`.

User must provide means `mu` and standard deviations `diag_stdev`.
Each batch member represents a random vector `(X_1,...,X_k)` of independent
random normals.
The mean of `X_i` is `mu[i]`, and the standard deviation is `diag_stdev[i]`.

##### Args:


*  <b>`mu`</b>: Rank `N + 1` floating point tensor with shape `[N1,...,Nb, k]`,
    `b >= 0`.
*  <b>`diag_stdev`</b>: Rank `N + 1` `Tensor` with same `dtype` and shape as `mu`,
    representing the standard deviations.  Must be positive.
*  <b>`validate_args`</b>: Whether to validate input with asserts.  If `validate_args`
    is `False`,
    and the inputs are invalid, correct behavior is not guaranteed.
*  <b>`allow_nan_stats`</b>: `Boolean`, default `False`.  If `False`, raise an
    exception if a statistic (e.g. mean/mode/etc...) is undefined for any
    batch member If `True`, batch members with valid parameters leading to
    undefined statistics will return NaN for this statistic.
*  <b>`name`</b>: The name to give Ops created by the initializer.

##### Raises:


*  <b>`TypeError`</b>: If `mu` and `diag_stdev` are different dtypes.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.allow_nan_stats` {#MultivariateNormalDiag.allow_nan_stats}

Python boolean describing behavior when a stat is undefined.

Stats return +/- infinity when it makes sense.  E.g., the variance
of a Cauchy distribution is infinity.  However, sometimes the
statistic is undefined, e.g., if a distribution's pdf does not achieve a
maximum within the support of the distribution, the mode is undefined.
If the mean is undefined, then by definition the variance is undefined.
E.g. the mean for Student's T for df = 1 is undefined (no clear way to say
it is either + or - infinity), so the variance = E[(X - mean)^2] is also
undefined.

##### Returns:


*  <b>`allow_nan_stats`</b>: Python boolean.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.batch_shape(name='batch_shape')` {#MultivariateNormalDiag.batch_shape}

Shape of a single sample from a single event index as a 1-D `Tensor`.

The product of the dimensions of the `batch_shape` is the number of
independent distributions of this kind the instance represents.

##### Args:


*  <b>`name`</b>: name to give to the op

##### Returns:


*  <b>`batch_shape`</b>: `Tensor`.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.cdf(value, name='cdf')` {#MultivariateNormalDiag.cdf}

Cumulative distribution function.

##### Args:


*  <b>`value`</b>: `float` or `double` `Tensor`.
*  <b>`name`</b>: The name to give this op.

##### Returns:


*  <b>`cdf`</b>: a `Tensor` of shape `sample_shape(x) + self.batch_shape` with
    values of type `self.dtype`.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.dtype` {#MultivariateNormalDiag.dtype}

The `DType` of `Tensor`s handled by this `Distribution`.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.entropy(name='entropy')` {#MultivariateNormalDiag.entropy}

Shanon entropy in nats.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.event_shape(name='event_shape')` {#MultivariateNormalDiag.event_shape}

Shape of a single sample from a single batch as a 1-D int32 `Tensor`.

##### Args:


*  <b>`name`</b>: name to give to the op

##### Returns:


*  <b>`event_shape`</b>: `Tensor`.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.from_params(cls, make_safe=True, **kwargs)` {#MultivariateNormalDiag.from_params}

Given (unconstrained) parameters, return an instantiated distribution.

Subclasses should implement a static method `_safe_transforms` that returns
a dict of parameter transforms, which will be used if `make_safe = True`.

Example usage:

```
# Let's say we want a sample of size (batch_size, 10)
shapes = MultiVariateNormalDiag.param_shapes([batch_size, 10])

# shapes has a Tensor shape for mu and sigma
# shapes == {
#   "mu": tf.constant([batch_size, 10]),
#   "sigma": tf.constant([batch_size, 10]),
# }

# Here we parameterize mu and sigma with the output of a linear
# layer. Note that sigma is unconstrained.
params = {}
for name, shape in shapes.items():
  params[name] = linear(x, shape[1])

# Note that you can forward other kwargs to the `Distribution`, like
# `allow_nan_stats` or `name`.
mvn = MultiVariateNormalDiag.from_params(**params, allow_nan_stats=True)
```

Distribution parameters may have constraints (e.g. `sigma` must be positive
for a `Normal` distribution) and the `from_params` method will apply default
parameter transforms. If a user wants to use their own transform, they can
apply it externally and set `make_safe=False`.

##### Args:


*  <b>`make_safe`</b>: Whether the `params` should be constrained. If True,
    `from_params` will apply default parameter transforms. If False, no
    parameter transforms will be applied.
*  <b>`**kwargs`</b>: dict of parameters for the distribution.

##### Returns:

  A distribution parameterized by possibly transformed parameters in
  `kwargs`.

##### Raises:


*  <b>`TypeError`</b>: if `make_safe` is `True` but `_safe_transforms` is not
    implemented directly for `cls`.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.get_batch_shape()` {#MultivariateNormalDiag.get_batch_shape}

Shape of a single sample from a single event index as a `TensorShape`.

Same meaning as `batch_shape`. May be only partially defined.

##### Returns:


*  <b>`batch_shape`</b>: `TensorShape`, possibly unknown.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.get_event_shape()` {#MultivariateNormalDiag.get_event_shape}

Shape of a single sample from a single batch as a `TensorShape`.

Same meaning as `event_shape`. May be only partially defined.

##### Returns:


*  <b>`event_shape`</b>: `TensorShape`, possibly unknown.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.is_continuous` {#MultivariateNormalDiag.is_continuous}




- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.is_reparameterized` {#MultivariateNormalDiag.is_reparameterized}




- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.log_cdf(value, name='log_cdf')` {#MultivariateNormalDiag.log_cdf}

Log cumulative distribution function.

##### Args:


*  <b>`value`</b>: `float` or `double` `Tensor`.
*  <b>`name`</b>: The name to give this op.

##### Returns:


*  <b>`logcdf`</b>: a `Tensor` of shape `sample_shape(x) + self.batch_shape` with
    values of type `self.dtype`.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.log_pdf(value, name='log_pdf')` {#MultivariateNormalDiag.log_pdf}

Log probability density function.

##### Args:


*  <b>`value`</b>: `float` or `double` `Tensor`.
*  <b>`name`</b>: The name to give this op.

##### Returns:


*  <b>`log_prob`</b>: a `Tensor` of shape `sample_shape(x) + self.batch_shape` with
    values of type `self.dtype`.

##### Raises:


*  <b>`AttributeError`</b>: if not `is_continuous`.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.log_pmf(value, name='log_pmf')` {#MultivariateNormalDiag.log_pmf}

Log probability mass function.

##### Args:


*  <b>`value`</b>: `float` or `double` `Tensor`.
*  <b>`name`</b>: The name to give this op.

##### Returns:


*  <b>`log_pmf`</b>: a `Tensor` of shape `sample_shape(x) + self.batch_shape` with
    values of type `self.dtype`.

##### Raises:


*  <b>`AttributeError`</b>: if `is_continuous`.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.log_prob(value, name='log_prob')` {#MultivariateNormalDiag.log_prob}

Log probability density/mass function (depending on `is_continuous`).

##### Args:


*  <b>`value`</b>: `float` or `double` `Tensor`.
*  <b>`name`</b>: The name to give this op.

##### Returns:


*  <b>`log_prob`</b>: a `Tensor` of shape `sample_shape(x) + self.batch_shape` with
    values of type `self.dtype`.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.log_sigma_det(name='log_sigma_det')` {#MultivariateNormalDiag.log_sigma_det}

Log of determinant of covariance matrix.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.mean(name='mean')` {#MultivariateNormalDiag.mean}

Mean.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.mode(name='mode')` {#MultivariateNormalDiag.mode}

Mode.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.mu` {#MultivariateNormalDiag.mu}




- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.name` {#MultivariateNormalDiag.name}

Name prepended to all ops created by this `Distribution`.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.param_shapes(cls, sample_shape, name='DistributionParamShapes')` {#MultivariateNormalDiag.param_shapes}

Shapes of parameters given the desired shape of a call to `sample()`.

Subclasses should override static method `_param_shapes`.

##### Args:


*  <b>`sample_shape`</b>: `Tensor` or python list/tuple. Desired shape of a call to
    `sample()`.
*  <b>`name`</b>: name to prepend ops with.

##### Returns:

  `dict` of parameter name to `Tensor` shapes.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.param_static_shapes(cls, sample_shape)` {#MultivariateNormalDiag.param_static_shapes}

param_shapes with static (i.e. TensorShape) shapes.

##### Args:


*  <b>`sample_shape`</b>: `TensorShape` or python list/tuple. Desired shape of a call
    to `sample()`.

##### Returns:

  `dict` of parameter name to `TensorShape`.

##### Raises:


*  <b>`ValueError`</b>: if `sample_shape` is a `TensorShape` and is not fully defined.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.parameters` {#MultivariateNormalDiag.parameters}

Dictionary of parameters used by this `Distribution`.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.pdf(value, name='pdf')` {#MultivariateNormalDiag.pdf}

Probability density function.

##### Args:


*  <b>`value`</b>: `float` or `double` `Tensor`.
*  <b>`name`</b>: The name to give this op.

##### Returns:


*  <b>`prob`</b>: a `Tensor` of shape `sample_shape(x) + self.batch_shape` with
    values of type `self.dtype`.

##### Raises:


*  <b>`AttributeError`</b>: if not `is_continuous`.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.pmf(value, name='pmf')` {#MultivariateNormalDiag.pmf}

Probability mass function.

##### Args:


*  <b>`value`</b>: `float` or `double` `Tensor`.
*  <b>`name`</b>: The name to give this op.

##### Returns:


*  <b>`pmf`</b>: a `Tensor` of shape `sample_shape(x) + self.batch_shape` with
    values of type `self.dtype`.

##### Raises:


*  <b>`AttributeError`</b>: if `is_continuous`.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.prob(value, name='prob')` {#MultivariateNormalDiag.prob}

Probability density/mass function (depending on `is_continuous`).

##### Args:


*  <b>`value`</b>: `float` or `double` `Tensor`.
*  <b>`name`</b>: The name to give this op.

##### Returns:


*  <b>`prob`</b>: a `Tensor` of shape `sample_shape(x) + self.batch_shape` with
    values of type `self.dtype`.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.sample(sample_shape=(), seed=None, name='sample')` {#MultivariateNormalDiag.sample}

Generate samples of the specified shape.

Note that a call to `sample()` without arguments will generate a single
sample.

##### Args:


*  <b>`sample_shape`</b>: 0D or 1D `int32` `Tensor`. Shape of the generated samples.
*  <b>`seed`</b>: Python integer seed for RNG
*  <b>`name`</b>: name to give to the op.

##### Returns:


*  <b>`samples`</b>: a `Tensor` with prepended dimensions `sample_shape`.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.sample_n(n, seed=None, name='sample_n')` {#MultivariateNormalDiag.sample_n}

Generate `n` samples.

##### Args:


*  <b>`n`</b>: `Scalar` `Tensor` of type `int32` or `int64`, the number of
    observations to sample.
*  <b>`seed`</b>: Python integer seed for RNG
*  <b>`name`</b>: name to give to the op.

##### Returns:


*  <b>`samples`</b>: a `Tensor` with a prepended dimension (n,).

##### Raises:


*  <b>`TypeError`</b>: if `n` is not an integer type.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.sigma` {#MultivariateNormalDiag.sigma}

Dense (batch) covariance matrix, if available.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.sigma_det(name='sigma_det')` {#MultivariateNormalDiag.sigma_det}

Determinant of covariance matrix.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.std(name='std')` {#MultivariateNormalDiag.std}

Standard deviation.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.validate_args` {#MultivariateNormalDiag.validate_args}

Python boolean indicated possibly expensive checks are enabled.


- - -

#### `tf.contrib.distributions.MultivariateNormalDiag.variance(name='variance')` {#MultivariateNormalDiag.variance}

Variance.


