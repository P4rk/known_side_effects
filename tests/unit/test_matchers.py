from parameterized import parameterized

from known_side_effects.matchers.types import (
    Any,
    NotNone,
    AnyString,
    AnyTuple,
    AnyDict,
    AnySet,
    AnyInt,
    AnyList,
    AnyObject,
    AnyBool,
)


@parameterized.expand([
    ('test',),
])
def test_any_match(item):
    assert Any().matches(item)


def test_any_mismatch():
    # impossible
    pass


@parameterized.expand([
    ('test',),
    (tuple(),),
    (dict(),),
    (set(),),
    (1,),
    ([],),
    (object(),),
])
def test_not_none_match(item):
    assert NotNone().matches(item)


@parameterized.expand([
    (None,),
])
def test_not_none_mismatch(item):
    assert not NotNone().matches(item)


@parameterized.expand([
    ('test',),
])
def test_any_string_match(item):
    assert AnyString().matches(item)


@parameterized.expand([
    (None,),
    (tuple(),),
    (dict(),),
    (set(),),
    (1,),
    ([],),
    (object(),),
])
def test_any_string_mismatch(item):
    assert not AnyString().matches(item)


@parameterized.expand([
    (tuple(),),
])
def test_any_tuple_match(item):
    assert AnyTuple().matches(item)


@parameterized.expand([
    (None,),
    ('test',),
    (dict(),),
    (set(),),
    (1,),
    ([],),
    (object(),),
])
def test_any_tuple_mismatch(item):
    assert not AnyTuple().matches(item)


@parameterized.expand([
    (dict(),),
])
def test_any_dict_match(item):
    assert AnyDict().matches(item)


@parameterized.expand([
    (None,),
    ('test',),
    (tuple(),),
    (set(),),
    (1,),
    ([],),
    (object(),),
])
def test_any_dict_mismatch(item):
    assert not AnyDict().matches(item)


@parameterized.expand([
    (set(),),
])
def test_any_set_match(item):
    assert AnySet().matches(item)


@parameterized.expand([
    (None,),
    ('test',),
    (tuple(),),
    (dict(),),
    (1,),
    ([],),
    (object(),),
])
def test_any_set_mismatch(item):
    assert not AnySet().matches(item)


@parameterized.expand([
    (1,),
])
def test_any_int_match(item):
    assert AnyInt().matches(item)


@parameterized.expand([
    (None,),
    ('test',),
    (tuple(),),
    (dict(),),
    (set(),),
    ([],),
    (object(),),
])
def test_any_int_mismatch(item):
    assert not AnyInt().matches(item)


@parameterized.expand([
    ([],),
])
def test_any_list_match(item):
    assert AnyList().matches(item)


@parameterized.expand([
    (None,),
    ('test',),
    (tuple(),),
    (dict(),),
    (set(),),
    (1,),
    (object(),),
])
def test_any_list_mismatch(item):
    assert not AnyList().matches(item)


@parameterized.expand([
    ('test',),
    (tuple(),),
    (dict(),),
    (set(),),
    (1,),
    ([],),
    (object(),),
    (None,),
])
def test_any_object_match(item):
    assert AnyObject().matches(item)


@parameterized.expand([
    (True,),
    (False,),
])
def test_any_bool_match(item):
    assert AnyBool().matches(item)


@parameterized.expand([
    (1,),
    (0,),
    (None,),
    ('test',),
    (tuple(),),
    (dict(),),
    (set(),),
    ([],),
    (object(),),
])
def test_any_bool_mismatch(item):
    assert not AnyBool().matches(item)

