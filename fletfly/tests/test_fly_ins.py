import pytest
from fletfly import fly_ins, fly_outs

# Dummy functions for testing
def f1(): pass
def f2(): pass
def f3(): pass

def test_single_callable():
    res = fly_ins(f1)
    assert len(res) == 1
    assert res[0]["func"] == f1
    assert res[0]["inheritable"] is True
    assert res[0]["apply_per_view"] is False

def test_multiple_callables_as_args():
    res = fly_outs(f1, f2)
    assert len(res) == 2
    assert res[0]["func"] == f1
    assert res[1]["func"] == f2
    assert res[0]["inheritable"] is False  # fly_outs default

def test_list_of_callables():
    res = fly_ins([f1, f2, f3])
    assert len(res) == 3
    assert [r["func"] for r in res] == [f1, f2, f3]

def test_callable_with_kwargs_tuple():
    res = fly_ins(f1, {"inheritable": False, "apply_per_view": True, "timeout": 30})
    assert len(res) == 1
    assert res[0]["func"] == f1
    assert res[0]["inheritable"] is False
    assert res[0]["apply_per_view"] is True
    assert res[0]["props"] == {"timeout": 30}

def test_list_of_tuples_with_kwargs():
    res = fly_ins([[f1, {"x": 1}], [f2, {"inheritable": False}]])
    assert len(res) == 2
    assert res[0]["props"] == {"x": 1}
    assert res[1]["inheritable"] is False

def test_deep_nested_unwrapping():
    res = fly_ins([[[f1]]])
    assert len(res) == 1
    assert res[0]["func"] == f1

def test_invalid_tuple_structure_raises_type_error():
    with pytest.raises(TypeError, match="Middleware tuple must be"):
        fly_ins((f1, "invalid_kwargs_type"))

def test_invalid_item_type_raises_type_error():
    with pytest.raises(TypeError, match="Expected a function or a list of functions"):
        fly_ins("string_is_not_allowed")

a1 = {"timeout": 10}
a2 = {"inheritable": False}

@pytest.mark.parametrize("args, expected_len, check_fn", [
    ((f1, a2), 1, lambda res: res[0]["func"] == f1 and res[0]["inheritable"] is False),
    
    (([f1, f2, f3],), 3, lambda res: [r["func"] for r in res] == [f1, f2, f3]),
    
    (([(f1,), f2],), 2, lambda res: res[0]["func"] == f1 and res[1]["func"] == f2),
    
    (([f1, (f2,), f2],), 3, lambda res: res[1]["func"] == f2),
    
    (([f1],), 1, lambda res: res[0]["func"] == f1),
    
    (([f1, a2],), 1, lambda res: res[0]["func"] == f1 and res[0]["inheritable"] is False),
    
    ((f1,), 1, lambda res: res[0]["func"] == f1),
    
    ((f1, f2), 2, lambda res: res[0]["func"] == f1 and res[1]["func"] == f2),
    
    ((f1, (f2, a2)), 2, lambda res: res[1]["props"] == {} and res[1]["inheritable"] is False),
    
    (((f1,), (f2,)), 2, lambda res: res[0]["func"] == f1 and res[1]["func"] == f2),
    
    (((f1,), f2), 2, lambda res: res[0]["func"] == f1),
    
    (([f1, a1], [f2, a2]), 2, lambda res: res[0]["props"] == {"timeout": 10} and res[1]["inheritable"] is False),
    
    (([],), 0, lambda res: res == []),
])
def test_fletfly_structural_cases(args, expected_len, check_fn):
    res = fly_ins(*args)
    assert len(res) == expected_len
    assert check_fn(res) is True
