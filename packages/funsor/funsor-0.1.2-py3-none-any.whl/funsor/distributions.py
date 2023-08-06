import math
from collections import OrderedDict

import pyro.distributions as dist
import torch
from pyro.distributions.util import broadcast_shape

import funsor.delta
import funsor.ops as ops
from funsor.affine import is_affine
from funsor.domains import bint, reals
from funsor.gaussian import Gaussian, cholesky_inverse
from funsor.interpreter import gensym, interpretation
from funsor.terms import Funsor, FunsorMeta, Number, Variable, eager, lazy, to_funsor
from funsor.torch import Tensor, align_tensors, ignore_jit_warnings, materialize, torch_stack


def numbers_to_tensors(*args):
    """
    Convert :class:`~funsor.terms.Number`s to :class:`funsor.torch.Tensor`s,
    using any provided tensor as a prototype, if available.
    """
    if any(isinstance(x, Number) for x in args):
        options = dict(dtype=torch.get_default_dtype())
        for x in args:
            if isinstance(x, Tensor):
                options = dict(dtype=x.data.dtype, device=x.data.device)
                break
        with ignore_jit_warnings():
            args = tuple(Tensor(torch.tensor(x.data, **options), dtype=x.dtype)
                         if isinstance(x, Number) else x
                         for x in args)
    return args


class DistributionMeta(FunsorMeta):
    """
    Wrapper to fill in default values and convert Numbers to Tensors.
    """
    def __call__(cls, *args, **kwargs):
        kwargs.update(zip(cls._ast_fields, args))
        args = cls._fill_defaults(**kwargs)
        args = numbers_to_tensors(*args)

        # If value was explicitly specified, evaluate under current interpretation.
        if 'value' in kwargs:
            return super(DistributionMeta, cls).__call__(*args)

        # Otherwise lazily construct a distribution instance.
        # This makes it cheaper to construct observations in minipyro.
        with interpretation(lazy):
            return super(DistributionMeta, cls).__call__(*args)


class Distribution(Funsor, metaclass=DistributionMeta):
    r"""
    Funsor backed by a PyTorch distribution object.

    :param \*args: Distribution-dependent parameters.  These can be either
        funsors or objects that can be coerced to funsors via
        :func:`~funsor.terms.to_funsor` . See derived classes for details.
    """
    dist_class = "defined by derived classes"

    def __init__(self, *args):
        params = tuple(zip(self._ast_fields, args))
        assert any(k == 'value' for k, v in params)
        inputs = OrderedDict()
        for name, value in params:
            assert isinstance(name, str)
            assert isinstance(value, Funsor)
            inputs.update(value.inputs)
        inputs = OrderedDict(inputs)
        output = reals()
        super(Distribution, self).__init__(inputs, output)
        self.params = params

    def __repr__(self):
        return '{}({})'.format(type(self).__name__,
                               ', '.join('{}={}'.format(*kv) for kv in self.params))

    def eager_reduce(self, op, reduced_vars):
        if op is ops.logaddexp and isinstance(self.value, Variable) and self.value.name in reduced_vars:
            return Number(0.)  # distributions are normalized
        return super(Distribution, self).eager_reduce(op, reduced_vars)

    @classmethod
    def eager_log_prob(cls, **params):
        inputs, tensors = align_tensors(*params.values())
        params = dict(zip(params, tensors))
        value = params.pop('value')
        data = cls.dist_class(**params).log_prob(value)
        return Tensor(data, inputs)


################################################################################
# Distribution Wrappers
################################################################################

class BernoulliProbs(Distribution):
    """
    Wraps :class:`pyro.distributions.Bernoulli` .

    :param Funsor probs: Probability of 1.
    :param Funsor value: Optional observation in ``{0,1}``.
    """
    dist_class = dist.Bernoulli

    @staticmethod
    def _fill_defaults(probs, value='value'):
        probs = to_funsor(probs)
        assert probs.dtype == "real"
        value = to_funsor(value, reals())
        return probs, value

    def __init__(self, probs, value=None):
        super(BernoulliProbs, self).__init__(probs, value)


@eager.register(BernoulliProbs, Tensor, Tensor)
def eager_bernoulli(probs, value):
    return BernoulliProbs.eager_log_prob(probs=probs, value=value)


class BernoulliLogits(Distribution):
    """
    Wraps :class:`pyro.distributions.Bernoulli` .

    :param Funsor logits: Log likelihood ratio of 1.
        This should equal ``log(p1 / p0)``.
    :param Funsor value: Optional observation in ``{0,1}``.
    """
    dist_class = dist.Bernoulli

    @staticmethod
    def _fill_defaults(logits, value='value'):
        logits = to_funsor(logits)
        assert logits.dtype == "real"
        value = to_funsor(value, reals())
        return logits, value

    def __init__(self, logits, value=None):
        super(BernoulliLogits, self).__init__(logits, value)


@eager.register(BernoulliLogits, Tensor, Tensor)
def eager_bernoulli_logits(logits, value):
    return BernoulliLogits.eager_log_prob(logits=logits, value=value)


def Bernoulli(probs=None, logits=None, value='value'):
    """
    Wraps :class:`pyro.distributions.Bernoulli` .

    This dispatches to either :class:`BernoulliProbs` or
    :class:`BernoulliLogits` to accept either ``probs`` or ``logits`` args.

    :param Funsor probs: Probability of 1.
    :param Funsor value: Optional observation in ``{0,1}``.
    """
    if probs is not None:
        return BernoulliProbs(probs, value)
    if logits is not None:
        return BernoulliLogits(logits, value)
    raise ValueError('Either probs or logits must be specified')


class Beta(Distribution):
    """
    Wraps :class:`pyro.distributions.Beta` .

    :param Funsor concentration1: Positive concentration parameter.
    :param Funsor concentration0: Positive concentration parameter.
    :param Funsor value: Optional observation in ``(0,1)``.
    """
    dist_class = dist.Beta

    @staticmethod
    def _fill_defaults(concentration1, concentration0, value='value'):
        concentration1 = to_funsor(concentration1, reals())
        concentration0 = to_funsor(concentration0, reals())
        value = to_funsor(value, reals())
        return concentration1, concentration0, value

    def __init__(self, concentration1, concentration0, value=None):
        super(Beta, self).__init__(concentration1, concentration0, value)


@eager.register(Beta, Tensor, Tensor, Tensor)
def eager_beta(concentration1, concentration0, value):
    return Beta.eager_log_prob(concentration1=concentration1,
                               concentration0=concentration0,
                               value=value)


@eager.register(Beta, Funsor, Funsor, Funsor)
def eager_beta(concentration1, concentration0, value):
    concentration = torch_stack((concentration0, concentration1))
    value = torch_stack((1 - value, value))
    return Dirichlet(concentration, value=value)


class Binomial(Distribution):
    """
    Wraps :class:`pyro.distributions.Binomial` .

    :param Funsor total_count: Total number of trials.
    :param Funsor probs: Probability of each positive trial.
    :param Funsor value: Optional integer observation (encoded as "real").
    """
    dist_class = dist.Binomial

    @staticmethod
    def _fill_defaults(total_count, probs, value='value'):
        total_count = to_funsor(total_count, reals())
        probs = to_funsor(probs)
        assert probs.dtype == "real"
        value = to_funsor(value, reals())
        return total_count, probs, value

    def __init__(self, total_count, probs, value=None):
        super(Binomial, self).__init__(total_count, probs, value)


@eager.register(Binomial, Tensor, Tensor, Tensor)
def eager_binomial(total_count, probs, value):
    return Binomial.eager_log_prob(total_count=total_count, probs=probs, value=value)


@eager.register(Binomial, Funsor, Funsor, Funsor)
def eager_binomial(total_count, probs, value):
    probs = torch_stack((1 - probs, probs))
    value = torch_stack((total_count - value, value))
    return Multinomial(total_count, probs, value=value)


class Categorical(Distribution):
    """
    Wraps :class:`pyro.distributions.Categorical` .

    :param Funsor probs: Probability vector over outcomes.
    :param Funsor value: Optional bouded integer observation.
    """
    dist_class = dist.Categorical

    @staticmethod
    def _fill_defaults(probs, value='value'):
        probs = to_funsor(probs)
        assert probs.dtype == "real"
        value = to_funsor(value, bint(probs.output.shape[0]))
        return probs, value

    def __init__(self, probs, value='value'):
        super(Categorical, self).__init__(probs, value)


@eager.register(Categorical, Funsor, Tensor)
def eager_categorical(probs, value):
    return probs[value].log()


@eager.register(Categorical, Tensor, Tensor)
def eager_categorical(probs, value):
    return Categorical.eager_log_prob(probs=probs, value=value)


@eager.register(Categorical, Tensor, Variable)
def eager_categorical(probs, value):
    value = materialize(value)
    return Categorical.eager_log_prob(probs=probs, value=value)


class Delta(Distribution):
    """
    Wraps :class:`pyro.distributions.Delta` .

    :param Funsor v: The unique point of concentration.
    :param Funsor log_density: Optional density (used by transformed
        distributions).
    :param Funsor value: Optional observation of similar domain as ``v``.
    """
    dist_class = dist.Delta

    @staticmethod
    def _fill_defaults(v, log_density=0, value='value'):
        v = to_funsor(v)
        log_density = to_funsor(log_density, reals())
        value = to_funsor(value, v.output)
        return v, log_density, value

    def __init__(self, v, log_density=0, value='value'):
        return super(Delta, self).__init__(v, log_density, value)


@eager.register(Delta, Tensor, Tensor, Tensor)
def eager_delta(v, log_density, value):
    # This handles event_dim specially, and hence cannot use the
    # generic Delta.eager_log_prob() method.
    assert v.output == value.output
    event_dim = len(v.output.shape)
    inputs, (v, log_density, value) = align_tensors(v, log_density, value)
    data = dist.Delta(v, log_density, event_dim).log_prob(value)
    return Tensor(data, inputs)


@eager.register(Delta, Funsor, Funsor, Variable)
@eager.register(Delta, Variable, Funsor, Variable)
def eager_delta(v, log_density, value):
    assert v.output == value.output
    return funsor.delta.Delta(value.name, v, log_density)


@eager.register(Delta, Variable, Funsor, Funsor)
def eager_delta(v, log_density, value):
    assert v.output == value.output
    return funsor.delta.Delta(v.name, value, log_density)


class Dirichlet(Distribution):
    """
    Wraps :class:`pyro.distributions.Dirichlet` .

    :param Funsor concentration: Positive concentration vector.
    :param Funsor value: Optional observation in the unit simplex.
    """
    dist_class = dist.Dirichlet

    @staticmethod
    def _fill_defaults(concentration, value='value'):
        concentration = to_funsor(concentration)
        assert concentration.dtype == "real"
        assert len(concentration.output.shape) == 1
        dim = concentration.output.shape[0]
        value = to_funsor(value, reals(dim))
        return concentration, value

    def __init__(self, concentration, value='value'):
        super(Dirichlet, self).__init__(concentration, value)


@eager.register(Dirichlet, Tensor, Tensor)
def eager_dirichlet(concentration, value):
    return Dirichlet.eager_log_prob(concentration=concentration, value=value)


class DirichletMultinomial(Distribution):
    """
    Wraps :class:`pyro.distributions.DirichletMultinomial` .

    :param Funsor concentration: Positive concentration vector.
    :param Funsor total_count: Total number of trials.
    :param Funsor value: Optional observation in the unit simplex.
    """
    dist_class = dist.DirichletMultinomial

    @staticmethod
    def _fill_defaults(concentration, total_count=1, value='value'):
        concentration = to_funsor(concentration)
        assert concentration.dtype == "real"
        assert len(concentration.output.shape) == 1
        total_count = to_funsor(total_count, reals())
        dim = concentration.output.shape[0]
        value = to_funsor(value, reals(dim))  # Should this be bint(total_count)?
        return concentration, total_count, value

    def __init__(self, concentration, total_count, value='value'):
        super(DirichletMultinomial, self).__init__(concentration, total_count, value)


@eager.register(DirichletMultinomial, Tensor, Tensor, Tensor)
def eager_dirichlet_multinomial(concentration, total_count, value):
    return DirichletMultinomial.eager_log_prob(
        concentration=concentration, total_count=total_count, value=value)


def LogNormal(loc, scale, value='value'):
    """
    Wraps :class:`pyro.distributions.LogNormal` .

    :param Funsor loc: Mean of the untransformed Normal distribution.
    :param Funsor scale: Standard deviation of the untransformed Normal
        distribution.
    :param Funsor value: Optional real observation.
    """
    loc, scale, y = Normal._fill_defaults(loc, scale, value)
    t = ops.exp
    x = t.inv(y)
    log_abs_det_jacobian = t.log_abs_det_jacobian(x, y)
    return Normal(loc, scale, x) - log_abs_det_jacobian


class Multinomial(Distribution):
    """
    Wraps :class:`pyro.distributions.Multinomial` .

    :param Funsor probs: Probability vector over outcomes.
    :param Funsor total_count: Total number of trials.
    :param Funsor value: Optional value in the unit simplex.
    """
    dist_class = dist.Multinomial

    @staticmethod
    def _fill_defaults(total_count, probs, value='value'):
        total_count = to_funsor(total_count, reals())
        probs = to_funsor(probs)
        assert probs.dtype == "real"
        assert len(probs.output.shape) == 1
        value = to_funsor(value, probs.output)
        return total_count, probs, value

    def __init__(self, total_count, probs, value=None):
        super(Multinomial, self).__init__(total_count, probs, value)


@eager.register(Multinomial, Tensor, Tensor, Tensor)
def eager_multinomial(total_count, probs, value):
    # Multinomial.log_prob() supports inhomogeneous total_count only by
    # avoiding passing total_count to the constructor.
    inputs, (total_count, probs, value) = align_tensors(total_count, probs, value)
    shape = broadcast_shape(total_count.shape + (1,), probs.shape, value.shape)
    probs = Tensor(probs.expand(shape), inputs)
    value = Tensor(value.expand(shape), inputs)
    total_count = Number(total_count.max().item())  # Used by distributions validation code.
    return Multinomial.eager_log_prob(total_count=total_count, probs=probs, value=value)


class Normal(Distribution):
    """
    Wraps :class:`pyro.distributions.Normal` .

    :param Funsor loc: Mean.
    :param Funsor scale: Standard deviation.
    :param Funsor value: Optional real observation.
    """
    dist_class = dist.Normal

    @staticmethod
    def _fill_defaults(loc, scale, value='value'):
        loc = to_funsor(loc, reals())
        scale = to_funsor(scale, reals())
        value = to_funsor(value, reals())
        return loc, scale, value

    def __init__(self, loc, scale, value='value'):
        super(Normal, self).__init__(loc, scale, value)


@eager.register(Normal, Tensor, Tensor, Tensor)
def eager_normal(loc, scale, value):
    return Normal.eager_log_prob(loc=loc, scale=scale, value=value)


@eager.register(Normal, Funsor, Tensor, Funsor)
def eager_normal(loc, scale, value):
    assert loc.output == reals()
    assert scale.output == reals()
    assert value.output == reals()
    if not is_affine(loc) or not is_affine(value):
        return None  # lazy

    info_vec = scale.data.new_zeros(scale.data.shape + (1,))
    precision = scale.data.pow(-2).reshape(scale.data.shape + (1, 1))
    log_prob = -0.5 * math.log(2 * math.pi) - scale.log().sum()
    inputs = scale.inputs.copy()
    var = gensym('value')
    inputs[var] = reals()
    gaussian = log_prob + Gaussian(info_vec, precision, inputs)
    return gaussian(**{var: value - loc})


class MultivariateNormal(Distribution):
    """
    Wraps :class:`pyro.distributions.MultivariateNormal` .

    :param Funsor loc: Mean vector.
    :param Funsor scale_tril: Lower Cholesky factor of the covariance matrix.
    :param Funsor value: Optional real vector observation.
    """
    dist_class = dist.MultivariateNormal

    @staticmethod
    def _fill_defaults(loc, scale_tril, value='value'):
        loc = to_funsor(loc)
        scale_tril = to_funsor(scale_tril)
        assert loc.dtype == 'real'
        assert scale_tril.dtype == 'real'
        assert len(loc.output.shape) == 1
        dim = loc.output.shape[0]
        assert scale_tril.output.shape == (dim, dim)
        value = to_funsor(value, loc.output)
        return loc, scale_tril, value

    def __init__(self, loc, scale_tril, value='value'):
        super(MultivariateNormal, self).__init__(loc, scale_tril, value)


@eager.register(MultivariateNormal, Tensor, Tensor, Tensor)
def eager_mvn(loc, scale_tril, value):
    return MultivariateNormal.eager_log_prob(loc=loc, scale_tril=scale_tril, value=value)


@eager.register(MultivariateNormal, Funsor, Tensor, Funsor)
def eager_mvn(loc, scale_tril, value):
    assert len(loc.shape) == 1
    assert len(scale_tril.shape) == 2
    assert value.output == loc.output
    if not is_affine(loc) or not is_affine(value):
        return None  # lazy

    info_vec = scale_tril.data.new_zeros(scale_tril.data.shape[:-1])
    precision = cholesky_inverse(scale_tril.data)
    scale_diag = Tensor(scale_tril.data.diagonal(dim1=-1, dim2=-2), scale_tril.inputs)
    log_prob = -0.5 * scale_diag.shape[0] * math.log(2 * math.pi) - scale_diag.log().sum()
    inputs = scale_tril.inputs.copy()
    var = gensym('value')
    inputs[var] = reals(scale_diag.shape[0])
    gaussian = log_prob + Gaussian(info_vec, precision, inputs)
    return gaussian(**{var: value - loc})


class Poisson(Distribution):
    """
    Wraps :class:`pyro.distributions.Poisson` .

    :param Funsor rate: Mean parameter.
    :param Funsor value: Optional integer observation (coded as "real").
    """
    dist_class = dist.Poisson

    @staticmethod
    def _fill_defaults(rate, value='value'):
        rate = to_funsor(rate)
        assert rate.dtype == "real"
        value = to_funsor(value, reals())
        return rate, value

    def __init__(self, rate, value=None):
        super().__init__(rate, value)


@eager.register(Poisson, Tensor, Tensor)
def eager_poisson(rate, value):
    return Poisson.eager_log_prob(rate=rate, value=value)


class Gamma(Distribution):
    """
    Wraps :class:`pyro.distributions.Gamma` .

    :param Funsor concentration: Positive concentration parameter.
    :param Funsor rate: Positive rate parameter.
    :param Funsor value: Optional positive observation.
    """
    dist_class = dist.Gamma

    @staticmethod
    def _fill_defaults(concentration, rate, value='value'):
        concentration = to_funsor(concentration)
        assert concentration.dtype == "real"
        rate = to_funsor(rate)
        assert rate.dtype == "real"
        value = to_funsor(value, reals())
        return concentration, rate, value

    def __init__(self, concentration, rate, value=None):
        super().__init__(concentration, rate, value)


@eager.register(Gamma, Tensor, Tensor, Tensor)
def eager_gamma(concentration, rate, value):
    return Gamma.eager_log_prob(concentration=concentration, rate=rate, value=value)


class VonMises(Distribution):
    """
    Wraps :class:`pyro.distributions.VonMises` .

    :param Funsor loc: A location angle.
    :param Funsor concentration: Positive concentration parameter.
    :param Funsor value: Optional angular observation.
    """
    dist_class = dist.VonMises

    @staticmethod
    def _fill_defaults(loc, concentration, value='value'):
        loc = to_funsor(loc)
        assert loc.dtype == "real"
        concentration = to_funsor(concentration)
        assert concentration.dtype == "real"
        value = to_funsor(value, reals())
        return loc, concentration, value

    def __init__(self, loc, concentration, value=None):
        super().__init__(loc, concentration, value)


@eager.register(VonMises, Tensor, Tensor, Tensor)
def eager_vonmises(loc, concentration, value):
    return VonMises.eager_log_prob(loc=loc, concentration=concentration, value=value)


__all__ = [
    'Bernoulli',
    'BernoulliLogits',
    'Beta',
    'Binomial',
    'Categorical',
    'Delta',
    'Dirichlet',
    'DirichletMultinomial',
    'Distribution',
    'Gamma',
    'LogNormal',
    'Multinomial',
    'MultivariateNormal',
    'Normal',
    'Poisson',
    'VonMises',
]
