from textwrap import dedent
import pytest

from modelx import *
from modelx.core.errors import NoneReturnedError


@pytest.fixture
def sample_space():

    space = new_model(name="samplemodel").new_space(name="samplespace")

    funcdef = """def func(x): return 2 * x"""

    space.new_cells(formula=funcdef)

    @defcells
    def fibo(x):
        if x == 0 or x == 1:
            return x
        else:
            return fibo(x - 1) + fibo[x - 2]

    @defcells
    def single_value():
        return 5

    @defcells
    def double(x):
        double[x] = 2 * x

    @defcells
    def triple(x):
        triple[x + 1] = 3 * x

    @defcells
    def quadruple(x):
        quadruple[x] = 4 * x
        return 4 * x

    @defcells
    def return_last(x):
        return return_last(x - 1)

    def func1(x):
        return 5 * x

    def func2(y):
        return 6 * y

    func1, func2 = defcells(func1, func2)

    @defcells
    def matchtest(x, y, z):
        return None

    matchtest.allow_none = True

    matchtest[1, 2, 3] = 123
    matchtest[1, 2, None] = 120
    matchtest[1, None, 3] = 103
    matchtest[None, 2, 3] = 23
    matchtest[1, None, None] = 100
    matchtest[None, 2, None] = 20
    matchtest[None, None, 3] = 3
    matchtest[None, None, None] = 0

    return space


def test_parent(sample_space):
    assert sample_space.func1.parent == sample_space


def test_defcells_funcs(sample_space):
    assert sample_space.func1[2] == 10 and sample_space.func2[2] == 12


def test_init_from_str(sample_space):
    assert sample_space.func[2] == 4


def test_getitem(sample_space):
    assert sample_space.fibo[10] == 55


def test_call(sample_space):
    assert sample_space.fibo(10) == 55


@pytest.mark.parametrize(
    "args, masked, value",
    [
        ((1, 2, 3), (1, 2, 3), 123),
        ((1, 2, 4), (1, 2, None), 120),
        ((1, 3, 3), (1, None, 3), 103),
        ((2, 2, 3), (None, 2, 3), 23),
        ((1, 3, 4), (1, None, None), 100),
        ((2, 2, 4), (None, 2, None), 20),
        ((2, 3, 3), (None, None, 3), 3),
        ((2, 3, 4), (None, None, None), 0),
    ],
)
def test_match(sample_space, args, masked, value):

    cells = sample_space.matchtest
    retargs, retvalue = cells.match(*args)

    assert retargs == masked and retvalue == value


def test_setitem(sample_space):
    sample_space.fibo[0] = 1
    assert sample_space.fibo[2] == 2


def test_setitem2(sample_space):
    sample_space.return_last[4] = 5
    assert sample_space.return_last(5) == 5


def test_setitem_str(sample_space):
    cells = sample_space.new_cells(formula="lambda s: 2 * s")
    cells["ABC"] = "DEF"
    assert cells["ABC"] == "DEF"


def test_setitem_in_cells(sample_space):
    assert sample_space.double[3] == 6


def test_setitem_in_wrong_cells(sample_space):
    with pytest.raises(KeyError):
        sample_space.triple[3]


def test_duplicate_assignment(sample_space):
    with pytest.raises(ValueError):
        sample_space.quadruple[4]


def test_clear_value(sample_space):
    sample_space.fibo[5]

    sample_space.fibo.clear(3)
    assert set(sample_space.fibo) == {0, 1, 2}


def test_clear_value_kwargs(sample_space):
    sample_space.fibo[5]

    sample_space.fibo.clear(x=3)
    assert set(sample_space.fibo) == {0, 1, 2}


def test_clear_all_values(sample_space):
    sample_space.fibo[5]

    assert set(sample_space.fibo) == {0, 1, 2, 3, 4, 5}

    sample_space.fibo.clear()
    assert set(sample_space.fibo) == set()


def test_clear_value_source(sample_space):

    space = sample_space

    f1 = dedent(
        """\
        def source(x):
            if x == 1:
                return 1
            else:
                return source(x - 1) + 1"""
    )

    f2 = dedent(
        """\
        def dependant(x):
            return 2 * source(x)"""
    )

    space.new_cells(formula=f1)
    space.new_cells(formula=f2)

    errors = []
    space.dependant(2)
    if not set(space.dependant) == {2}:
        errors.append("error with dependant")
    if not set(space.source) == {1, 2}:
        errors.append("error with source")

    space.source.clear(1)
    if not set(space.source) == set():
        errors.append("clear error with source")
    if not set(space.dependant) == set():
        errors.append("clear error with dependant")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_clear_formula(sample_space):

    space = sample_space
    f1 = dedent(
        """\
        def clear_source(x):
            if x == 1:
                return 1
            else:
                return clear_source(x - 1) + 1"""
    )

    f2 = dedent(
        """\
        def clear_dependant(x):
            return 2 * clear_source(x)"""
    )

    source = space.new_cells(formula=f1)
    dependant = space.new_cells(formula=f2)

    dependant(2)
    assert set(dependant) == {2}
    assert set(source) == {1, 2}

    del source.formula
    assert set(source) == set()
    assert set(dependant) == set()


def test_set_formula(sample_space):

    space = sample_space
    f1 = dedent(
        """\
        def clear_source(x):
            if x == 1:
                return 1
            else:
                return clear_source(x - 1) + 1"""
    )

    f2 = dedent(
        """\
        def clear_dependant(x):
            return 2 * clear_source(x)"""
    )

    f3 = dedent(
        """\
        def replace_source(x):
            if x == 1:
                return 2
            else:
                return clear_source(x - 1) + 1"""
    )

    source = space.new_cells(formula=f1)
    dependant = space.new_cells(formula=f2)

    result = dependant(2)
    assert set(dependant) == {2}
    assert set(source) == {1, 2}
    assert result == 4

    source.formula = f3
    result = dependant(2)
    assert set(source) == {1, 2}
    assert set(dependant) == {2}
    assert result == 6


def test_call_single_value(sample_space):
    assert sample_space.single_value() == 5


def test_single_value(sample_space):
    assert sample_space.single_value == 5


def test_parameters(sample_space):

    space = sample_space
    assert space.fibo.parameters == ("x",)
    assert space.single_value.parameters == ()
    assert space.matchtest.parameters == ("x", "y", "z")


# --------------------------------------------------------------------------
# Test fullname


def test_fullname(sample_space):
    assert (
        sample_space.fibo.fullname
        == "samplemodel.samplespace.fibo"
    )


def test_fullname_omit_model(sample_space):
    assert (
        sample_space.fibo._impl.get_fullname(omit_model=True)
        == "samplespace.fibo"
    )


# --------------------------------------------------------------------------
# Test errors


def test_none_returned_error():

    errfunc = dedent(
        """\
        def return_none(x, y):
            return None"""
    )

    space = new_model(name="ErrModel").new_space(name="ErrSpace")
    cells = space.new_cells(formula=errfunc)
    cells.allow_none = False
    with pytest.raises(NoneReturnedError) as errinfo:
        cells(1, 3)

    errmsg = dedent(
        """\
        None returned from ErrModel.ErrSpace.return_none(x=1, y=3).
        Call stack traceback:
        0: ErrModel.ErrSpace.return_none(x=1, y=3)"""
    )

    assert errinfo.value.args[0] == errmsg


def test_zerodiv():

    from modelx.core.errors import RewindStackError

    zerodiv = dedent(
        """\
        def zerodiv(x):
            if x == 3:
                return x / 0
            else:
                return zerodiv(x + 1)"""
    )

    space = new_model().new_space(name="ZeroDiv")
    cells = space.new_cells(formula=zerodiv)

    with pytest.raises(RewindStackError):
        cells(0)
