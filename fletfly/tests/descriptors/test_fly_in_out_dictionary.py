# fletfly/tests/descriptors/test_fly_in_out_dictionary.py
import pytest
from fletfly import fly_in, fly_out, _FlyInOutDict
# Dummy function to be used as a middleware in tests
def dummy_middleware(page, **kwargs):
    pass

def test_fly_in_direct_call_with_kwargs():

    result = fly_in(dummy_middleware, role="user", requires_auth=True)
    
    assert isinstance(result, _FlyInOutDict)
    assert result["func"] == dummy_middleware
    # inheritable defaults to True in fly_in
    assert result["inheritable"] is True
    assert result["apply_per_view"] is False
    # Verify that kwargs are collected correctly
    assert result["props"] == {"role": "user", "requires_auth": True}
fly_in()
def test_fly_out_direct_call_with_kwargs():
    """
    Test direct invocation of fly_out with custom configuration 
    (inheritable should default to False here).
    """
    result = fly_out(dummy_middleware, clear_cache=True)
    
    assert isinstance(result, _FlyInOutDict)
    assert result["func"] == dummy_middleware
    # inheritable defaults to False in fly_out
    assert result["inheritable"] is False
    assert result["apply_per_view"] is False
    assert result["props"] == {"clear_cache": True}

def test_direct_call_overriding_defaults():
    """
    Test overriding default values (inheritable and apply_per_view) 
    by passing them as Keyword Arguments.
    """
    # Overriding defaults for fly_in
    res_in = fly_in(dummy_middleware, inheritable=False, apply_per_view=True, extra_data="test")
    
    assert res_in["inheritable"] is False
    assert res_in["apply_per_view"] is True
    # Ensure core arguments are not pulled into kwargs
    assert res_in["props"] == {"extra_data": "test"}

    # Overriding defaults for fly_out
    res_out = fly_out(dummy_middleware, inheritable=True, apply_per_view=True, save_state=False)
    
    assert res_out["inheritable"] is True
    assert res_out["apply_per_view"] is True
    assert res_out["props"] == {"save_state": False}

def test_direct_call_positional_arguments():
    """
    Test passing expected arguments (inheritable and apply_per_view) 
    positionally based on the expected dict order.
    """
    # Expected order: inheritable then apply_per_view
    # Passing False for inheritable and True for apply_per_view positionally
    result = fly_in(dummy_middleware, False, True, role="admin")
    
    print(result)
    assert result["inheritable"] is False
    assert result["apply_per_view"] is True
    assert result["props"] == {"role": "admin"}

def test_direct_call_type_validation():
    """
    Test Type Checking for expected arguments.
    """
    # 'inheritable' expects a bool, passing a string to trigger a TypeError
    with pytest.raises(TypeError) as excinfo:
        fly_in(dummy_middleware, inheritable="True")
    
    assert "must be of type bool" in str(excinfo.value)