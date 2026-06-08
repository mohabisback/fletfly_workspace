# fletfly/tests/descriptors/test_fly_in.py
import pytest
from fletfly import Airway, fly_in, _FlyIn

# --- Case a: Instance setting ---
def test_fly_in_set_value_on_instance():
    """Verify setting value on instance updates private list while class descriptor remains intact."""
    aw = Airway()
    def dummy_func(page): pass
    aw.fly_in = dummy_func
    assert isinstance(Airway.fly_in, _FlyIn)
    assert aw.fly_ins[0]["func"] == dummy_func

# --- Class Decoration Cases (6 Tests) ---
def test_fly_in_decorator_on_class():
    """Case b: @item on class."""
    @fly_in
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_fly_in")[0].get("inheritable", "not there") is True
    assert getattr(SampleClass, "_fletfly_fly_in")[0].get("apply_per_view", "not there") is False
    assert getattr(SampleClass, "_fletfly_fly_in")[0].get("props", "not there") == {}


def test_fly_in_decorator_with_args_on_class():
    """Case c: @item(arg, arg) on class."""
    @fly_in(inheritable=True)
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_fly_in")[0].get("inheritable", "not there") is True
    assert getattr(SampleClass, "_fletfly_fly_in")[0].get("apply_per_view", "not there") is False
    assert getattr(SampleClass, "_fletfly_fly_in")[0].get("props", "not there") == {}

def test_fly_in_via_class_attribute_on_class():
    """Case d: @Airway.item on class."""
    @Airway.fly_in
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_fly_in")[0].get("inheritable", "not there") is True
    assert getattr(SampleClass, "_fletfly_fly_in")[0].get("apply_per_view", "not there") is False
    assert getattr(SampleClass, "_fletfly_fly_in")[0].get("props", "not there") == {}


def test_fly_in_via_class_attribute_with_args_on_class():
    """Case e: @Airway.fly_in(arg, arg) on class."""
    @Airway.fly_in(inheritable=True, role="user")
    class SampleClass: pass

    assert getattr(SampleClass, "_fletfly_fly_in")[0].get("inheritable", "not there") is True
    assert getattr(SampleClass, "_fletfly_fly_in")[0].get("apply_per_view", "not there") is False
    assert getattr(SampleClass, "_fletfly_fly_in")[0].get("props", "not there") == {"role":"user"}

    list(Airway._pending_airways)[0].props == {"role":"user"}
    
# --- Function Decoration Cases (6 Tests) ---
def test_fly_in_decorator_on_function():
    """Case b_func: @item on function."""
    @fly_in
    def sample_func(page): pass

    assert getattr(sample_func, "_fletfly_fly_in")[0].get("inheritable", "not there") is True
    assert getattr(sample_func, "_fletfly_fly_in")[0].get("apply_per_view", "not there") is False
    assert getattr(sample_func, "_fletfly_fly_in")[0].get("props", "not there") == {}


def test_fly_in_decorator_with_args_on_function():
    """Case c_func: @item(arg, arg) on function."""
    @fly_in(inheritable=True, role="user")
    def sample_func(page): pass

    assert getattr(sample_func, "_fletfly_fly_in")[0].get("inheritable", "not there") is True
    assert getattr(sample_func, "_fletfly_fly_in")[0].get("apply_per_view", "not there") is False
    assert getattr(sample_func, "_fletfly_fly_in")[0].get("props", "not there") == {"role":"user"}

    
def test_fly_in_via_class_attribute_on_function():
    """Case d_func: @Airway.item on function."""
    @Airway.fly_in
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_fly_in")[0].get("inheritable", "not there") is True
    assert getattr(sample_func, "_fletfly_fly_in")[0].get("apply_per_view", "not there") is False
    assert getattr(sample_func, "_fletfly_fly_in")[0].get("props", "not there") == {}


def test_fly_in_via_class_attribute_with_args_on_function():
    """Case e_func: @Airway.fly_in(arg, arg) on function."""
    @Airway.fly_in(inheritable=True, role="user")
    def sample_func(page): pass

    assert getattr(sample_func, "_fletfly_fly_in")[0].get("inheritable", "not there") is True
    assert getattr(sample_func, "_fletfly_fly_in")[0].get("apply_per_view", "not there") is False
    assert getattr(sample_func, "_fletfly_fly_in")[0].get("props", "not there") == {"role":"user"}    

def test_fly_in_via_instance_attribute_with_args_on_function():
    """Case g_func: @Airway().item() on function."""
    def sample_func(page): pass
    aw = Airway()
    aw.fly_in(sample_func, inheritable=True, role="user")
    assert aw.fly_ins[0]["func"] == sample_func
    assert aw.fly_ins[0]["inheritable"] == True
    assert aw.fly_ins[0]["props"]== {"role":"user"}
    assert aw.fly_ins[0]["props"].get("inheritable", "not there") == "not there"
