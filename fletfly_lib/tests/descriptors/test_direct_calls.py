# fletfly/tests/descriptors/test_direct_calls.py
# fletfly/tests/test_descriptors.py
import pytest
from fletfly import (
    layout, 
    view, 
    fly_in, 
    fly_out, 
    child, 
    Route, 
    UseFunc, 
    use
)

def test_layout_direct_call_returns_dict():
    """Test that calling layout directly returns a UseFunc with correct config."""
    def sample_view():
        pass
        
    res = layout(sample_view, hero=True, override=False, role="user")
    assert isinstance(res, UseFunc)
    assert res["func"] is sample_view
    assert res["props"] == {"role":"user"}


def test_fly_in_direct_call_with_cls_keyword():
    """Test that passing 'cls' as a keyword argument converts it to 'func' properly."""
    def dummy_func(): pass
    aw = Route()
    res1 = use.fly_in(func=dummy_func, inheritable=True, apply_per_view=True, role="user")
    res2 = aw.fly_out(dummy_func, True, True, role="user")
 
    assert isinstance(res1, UseFunc)
    assert res1["func"] is dummy_func
    assert res1["inheritable"] is True
    assert res1["apply_per_view"] is True
    assert res1.get("override", None) is None
    assert res1["props"].get("role") == "user"
    assert res1["props"].get("override", "not there") == "not there"

    assert isinstance(res2, Route)
    assert res2.fly_outs[0]["func"] is dummy_func
    assert res2.fly_outs[0]["inheritable"] is True
    assert res2.fly_outs[0]["apply_per_view"] is True
    assert res2.fly_outs[0].get("override", None) is None
    assert res2.fly_outs[0]["props"].get("role") == "user"
    assert res2.fly_outs[0]["props"].get("override", "not there") == "not there"


def test_descriptor_bound_instance_setattr():
    """Test that calling a descriptor on an Route instance attaches the wrapped dict."""
    class CustomRoute(Route):
        pass
        
    aw = CustomRoute()
    
    def target_view():
        pass
        
    # Direct call through instance triggers instance-level assignment
    res1 = aw.view(target_view, hero=True, role="user")
    assert isinstance(res1, Route)
    res2 = view(target_view, hero=True, role="user")
    assert isinstance(res2, UseFunc)
    assert aw._view["func"] == target_view
    assert aw.view_hero == True
    assert res2["props"].get("hero", "not there") == "not there"
    assert res2["props"].get("role") == "user"
    assert getattr(aw, "role", None) is None


def test_pre_process_duplicate_func_raises_error():
    """Test that passing the expected function as positional and keyword raises ValueError."""
    def sample_func():
        pass
        
    with pytest.raises(ValueError, match="Can't have 2 'func' in arguments"):
        layout(sample_func, func=sample_func)


def test_pre_process_invalid_type_raises_type_error():
    """Test that passing invalid types for expected arguments raises TypeError."""
    def sample_func():
        pass
        
    # 'hero' argument expects a boolean value
    with pytest.raises(TypeError, match="Argument.*expected to be of type bool"):
        view(sample_func, hero="not-a-bool")
