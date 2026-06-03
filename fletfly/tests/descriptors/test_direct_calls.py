# fletfly/tests/descriptors/test_direct_calls.py
# fletfly/tests/test_descriptors.py
import pytest
from fletfly import (
    layout, 
    build, 
    fly_in, 
    fly_out, 
    subway, 
    Airway, 
    _BuildLayoutDict, 
    _FlyInOutDict
)

def test_layout_direct_call_returns_dict():
    """Test that calling layout directly returns a _BuildLayoutDict with correct config."""
    def sample_view():
        pass
        
    res = layout(sample_view, hero=True, override=False, role="user")
    assert isinstance(res, _BuildLayoutDict)
    assert res["func"] is sample_view
    assert res["kwargs"] == {"role":"user"}


def test_fly_in_direct_call_with_class():
    """Test that passing 'cls' as a keyword argument converts it to 'func' properly."""
    class SampleComponent:
        pass
    
    aw = Airway()
def test_fly_in_direct_call_with_class():
    """Test that passing a class instead of a function raises ValueError."""
    class SampleComponent:
        pass
    
    aw = Airway()
    
    # Each call must be validated in an isolated block
    with pytest.raises(ValueError):
        fly_in(cls=SampleComponent, inheritable=True, apply_per_view=True)
        
    with pytest.raises(ValueError):
        fly_out(SampleComponent, True, True)
        
    with pytest.raises(ValueError):
        aw.fly_in(cls=SampleComponent, inheritable=True, apply_per_view=True)
        
    with pytest.raises(ValueError):
        aw.fly_out(SampleComponent, True, True)

def test_fly_in_direct_call_with_cls_keyword():
    """Test that passing 'cls' as a keyword argument converts it to 'func' properly."""
    def dummy_func(): pass
    aw = Airway()
    res1 = fly_in(cls=dummy_func, inheritable=True, apply_per_view=True, role="user")
    res2 = aw.fly_out(dummy_func, True, True, role="user")
 
    assert isinstance(res1, _FlyInOutDict)
    assert res1["func"] is dummy_func
    assert res1["inheritable"] is True
    assert res1["apply_per_view"] is True
    assert res1.get("override", None) is None
    assert res1["kwargs"].get("role") == "user"
    assert res1["kwargs"].get("override", "not there") == "not there"

    assert isinstance(res2, _FlyInOutDict)
    assert res2["func"] is dummy_func
    assert res2["inheritable"] is True
    assert res2["apply_per_view"] is True
    assert res2.get("override", None) is None
    assert res2["kwargs"].get("role") == "user"
    assert res2["kwargs"].get("override", "not there") == "not there"


def test_descriptor_bound_instance_setattr():
    """Test that calling a descriptor on an Airway instance attaches the wrapped dict."""
    class CustomAirway(Airway):
        pass
        
    aw = CustomAirway()
    
    def target_build():
        pass
        
    # Direct call through instance triggers instance-level assignment
    res = aw.build(target_build, hero=True, role="user")
    assert isinstance(res, _BuildLayoutDict)
    assert aw._build == res
    assert aw.build_hero == True
    assert res["kwargs"].get("hero", "not there") == "not there"
    assert res["kwargs"].get("role") == "user"
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
    with pytest.raises(TypeError, match="Argument.*must be of type bool"):
        build(sample_func, hero="not-a-bool")


def test_subway_descriptor_direct_call_validation():
    """Test that calling subway directly without parents or instance raises ValueError."""
    def sample_route():
        pass
        
    with pytest.raises(ValueError, match="subway\\(\\) must have parents arguments"):
        subway(sample_route, path="/home")