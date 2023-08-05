import modelx as mx
from modelx.core.errors import DeepReferenceError
import pytest

def test_max_recursion():

    maxdepth = 65000
    m, s = mx.new_model(), mx.new_space()

    @mx.defcells
    def foo(x):
        if x == 0:
            return 0
        else:
            return foo(x-1) + 1

    assert foo(maxdepth) == maxdepth


def test_maxout_recursion():

    maxdepth = 65001
    m, s = mx.new_model(), mx.new_space()

    @mx.defcells
    def foo(x):
        if x == 0:
            return 0
        else:
            return foo(x-1) + 1

    with pytest.raises(DeepReferenceError):
        foo(maxdepth)
