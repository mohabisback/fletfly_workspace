# fletfly/tests/descriptors/test_fly_out.py
import pytest
from fletfly import Route, General, fly_out, _FlyOut

# --- Case a: Instance setting ---
def test_fly_out_set_value_on_instance():
    """Verify setting value on instance updates private list while class descriptor remains intact."""
    aw = Route()
    def dummy_func(page): pass
    aw.fly_out = dummy_func
    assert isinstance(Route.fly_out, _FlyOut)
    assert aw.fly_outs[0]["func"] == dummy_func

# --- Class Decoration Cases (6 Tests) ---
def test_fly_out_decorator_on_class():
    """Case b: @item on class."""
    @fly_out
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_fly_out")[0].get("inheritable", "not there") is False
    assert getattr(SampleClass, "_fletfly_fly_out")[0].get("apply_per_view", "not there") is False
    assert getattr(SampleClass, "_fletfly_fly_out")[0].get("props", "not there") == {}


def test_fly_out_decorator_with_args_on_class():
    """Case c: @item(arg, arg) on class."""
    @fly_out(inheritable=True)
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_fly_out")[0].get("inheritable", "not there") is True
    assert getattr(SampleClass, "_fletfly_fly_out")[0].get("apply_per_view", "not there") is False
    assert getattr(SampleClass, "_fletfly_fly_out")[0].get("props", "not there") == {}

def test_fly_out_via_class_attribute_on_class():
    """Case d: @Route.item on class."""
    @Route.fly_out
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_fly_out")[0].get("inheritable", "not there") is False
    assert getattr(SampleClass, "_fletfly_fly_out")[0].get("apply_per_view", "not there") is False
    assert getattr(SampleClass, "_fletfly_fly_out")[0].get("props", "not there") == {}


def test_fly_out_via_class_attribute_with_args_on_class():
    """Case e: @Route.fly_out(arg, arg) on class."""
    @Route.fly_out(inheritable=True, role="user")
    class SampleClass: pass

    assert getattr(SampleClass, "_fletfly_fly_out")[0].get("inheritable", "not there") is True
    assert getattr(SampleClass, "_fletfly_fly_out")[0].get("apply_per_view", "not there") is False
    assert getattr(SampleClass, "_fletfly_fly_out")[0].get("props", "not there") == {"role":"user"}

# --- Function Decoration Cases (6 Tests) ---
def test_fly_out_decorator_on_function():
    """Case b_func: @item on function."""
    @fly_out
    def sample_func(page): pass

    assert getattr(sample_func, "_fletfly_fly_out")[0].get("inheritable", "not there") is False
    assert getattr(sample_func, "_fletfly_fly_out")[0].get("apply_per_view", "not there") is False
    assert getattr(sample_func, "_fletfly_fly_out")[0].get("props", "not there") == {}


def test_fly_out_decorator_with_args_on_function():
    """Case c_func: @item(arg, arg) on function."""
    @fly_out(inheritable=True, role="user")
    def sample_func(page): pass

    assert getattr(sample_func, "_fletfly_fly_out")[0].get("inheritable", "not there") is True
    assert getattr(sample_func, "_fletfly_fly_out")[0].get("apply_per_view", "not there") is False
    assert getattr(sample_func, "_fletfly_fly_out")[0].get("props", "not there") == {"role":"user"}

    
def test_fly_out_via_class_attribute_on_function():
    """Case d_func: @Route.item on function."""
    @Route.fly_out
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_fly_out")[0].get("inheritable", "not there") is False
    assert getattr(sample_func, "_fletfly_fly_out")[0].get("apply_per_view", "not there") is False
    assert getattr(sample_func, "_fletfly_fly_out")[0].get("props", "not there") == {}


def test_fly_out_via_class_attribute_with_args_on_function():
    """Case e_func: @Route.fly_out(arg, arg) on function."""
    @Route.fly_out(inheritable=True, role="user")
    def sample_func(page): pass

    assert getattr(sample_func, "_fletfly_fly_out")[0].get("inheritable", "not there") is True
    assert getattr(sample_func, "_fletfly_fly_out")[0].get("apply_per_view", "not there") is False
    assert getattr(sample_func, "_fletfly_fly_out")[0].get("props", "not there") == {"role":"user"}

def test_fly_out_via_instance_attribute_with_args_on_function():
    """Case g_func: @Route().item() on function."""
    def sample_func(page): pass
    aw = Route()
    aw.fly_out(sample_func, inheritable=True, role="user")
    assert aw.fly_outs[0]["func"] == sample_func
    assert aw.fly_outs[0]["inheritable"] == True
    assert aw.fly_outs[0]["props"]== {"role":"user"}
    assert aw.fly_outs[0]["props"].get("inheritable", "not there") == "not there"
