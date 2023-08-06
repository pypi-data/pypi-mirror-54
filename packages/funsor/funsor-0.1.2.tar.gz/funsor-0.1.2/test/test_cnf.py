import itertools
from collections import OrderedDict

import pytest
import torch  # noqa F403

from funsor import ops
from funsor.cnf import Contraction
from funsor.domains import bint  # noqa F403
from funsor.domains import reals
from funsor.einsum import einsum, naive_plated_einsum
from funsor.interpreter import interpretation, reinterpret
from funsor.terms import Number, eager, normalize, reflect
from funsor.testing import assert_close, check_funsor, make_einsum_example, random_tensor
from funsor.torch import Tensor
from funsor.util import quote

EINSUM_EXAMPLES = [
    ("a,b->", ''),
    ("ab,a->", ''),
    ("a,a->", ''),
    ("a,a->a", ''),
    ("ab,bc,cd->da", ''),
    ("ab,cd,bc->da", ''),
    ("a,a,a,ab->ab", ''),
    ('i->', 'i'),
    (',i->', 'i'),
    ('ai->', 'i'),
    (',ai,abij->', 'ij'),
    ('a,ai,bij->', 'ij'),
    ('ai,abi,bci,cdi->', 'i'),
    ('aij,abij,bcij->', 'ij'),
    ('a,abi,bcij,cdij->', 'ij'),
]


@pytest.mark.parametrize('equation,plates', EINSUM_EXAMPLES)
@pytest.mark.parametrize('backend', ['torch', 'pyro.ops.einsum.torch_log'])
@pytest.mark.parametrize('einsum_impl', [einsum, naive_plated_einsum])
def test_normalize_einsum(equation, plates, backend, einsum_impl):
    inputs, outputs, sizes, operands, funsor_operands = make_einsum_example(equation)

    with interpretation(reflect):
        expr = einsum_impl(equation, *funsor_operands, backend=backend, plates=plates)

    with interpretation(normalize):
        transformed_expr = reinterpret(expr)

    assert isinstance(transformed_expr, Contraction)
    check_funsor(transformed_expr, expr.inputs, expr.output)

    assert all(isinstance(v, (Number, Tensor, Contraction)) for v in transformed_expr.terms)

    with interpretation(normalize):
        transformed_expr2 = reinterpret(transformed_expr)

    assert transformed_expr2 is transformed_expr  # check normalization

    with interpretation(eager):
        actual = reinterpret(transformed_expr)
        expected = reinterpret(expr)

    assert_close(actual, expected, rtol=1e-4)

    actual = eval(quote(expected))  # requires torch, bint
    assert_close(actual, expected)


@pytest.mark.parametrize("x_shape", [(), (1,), (3,), (1, 1), (1, 3), (2, 1), (2, 3)], ids=str)
@pytest.mark.parametrize("y_shape", [(), (1,), (3,), (1, 1), (1, 3), (2, 1), (2, 3)], ids=str)
@pytest.mark.parametrize("x_inputs,y_inputs", [
    ("", ""),
    ("i", ""),
    ("", "i"),
    ("j", "i"),
    ("ij", "i"),
    ("i", "ik"),
    ("ij", "ik"),
])
@pytest.mark.parametrize("red_op,bin_op", [(ops.add, ops.mul), (ops.logaddexp, ops.add)], ids=str)
def test_eager_contract_tensor_tensor(red_op, bin_op, x_inputs, x_shape, y_inputs, y_shape):
    inputs = OrderedDict([("i", bint(4)), ("j", bint(5)), ("k", bint(6))])
    x_inputs = OrderedDict((k, v) for k, v in inputs.items() if k in x_inputs)
    y_inputs = OrderedDict((k, v) for k, v in inputs.items() if k in y_inputs)
    x = random_tensor(x_inputs, reals(*x_shape))
    y = random_tensor(y_inputs, reals(*y_shape))

    xy = bin_op(x, y)
    all_vars = frozenset(x.inputs).union(y.inputs)
    for n in range(len(all_vars)):
        for reduced_vars in map(frozenset, itertools.combinations(all_vars, n)):
            print(f"reduced_vars = {reduced_vars}")
            expected = xy.reduce(red_op, reduced_vars)
            actual = Contraction(red_op, bin_op, reduced_vars, (x, y))
            assert_close(actual, expected, atol=1e-4, rtol=1e-4)
