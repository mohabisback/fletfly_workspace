# fletfly/tests/descriptors/test_fly_out.py
import pytest
from fletfly import Airway, fly_out, _FlyOut

# --- Case a: Instance setting ---
def test_fly_out_set_value_on_instance():
    """Verify setting value on instance updates private list while class descriptor remains intact."""
    aw = Airway()
    def dummy_func(page): pass
    aw.fly_out = dummy_func
    assert isinstance(Airway.fly_out, _FlyOut)
    assert dummy_func in aw.fly_outs

# --- Class Decoration Cases (6 Tests) ---
def test_fly_out_decorator_on_class():
    """Case b: @item on class."""
    @fly_out
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_fly_out", False) is True

def test_fly_out_decorator_with_args_on_class():
    """Case c: @item(arg, arg) on class."""
    @fly_out(inheritable=True)
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_fly_out", None) is True
    assert getattr(SampleClass, "inheritable", None) is None
    assert getattr(SampleClass, "inheritable_clsattr", None) is None
    assert getattr(SampleClass, "apply_per_view", None) is None
    assert getattr(SampleClass, "apply_per_view_clsattr", None) is None
def test_fly_out_via_class_attribute_on_class():
    """Case d: @Airway.item on class."""
    @Airway.fly_out
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_fly_out", False) is True

def test_fly_out_via_class_attribute_with_args_on_class():
    """Case e: @Airway.fly_out(arg, arg) on class."""
    @Airway.fly_out(inheritable=True, role="user")
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_fly_out", None) is True
    assert getattr(SampleClass, "_fletfly_inheritable", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_role", "not there") == "not there"
    assert getattr(SampleClass, "role", "not there") == "user"
def test_fly_out_via_instance_attribute_on_class_raises_error():
    """Case f: @Airway().item on class -> error."""
    with pytest.raises(ValueError):
        @Airway().fly_out
        class SampleClass: pass

def test_fly_out_via_instance_attribute_with_args_on_class_raises_error():
    """Case g: @Airway().item() on class -> error."""
    with pytest.raises(ValueError):
        @Airway().fly_out(inheritable=True)
        class SampleClass: pass

# --- Function Decoration Cases (6 Tests) ---
def test_fly_out_decorator_on_function():
    """Case b_func: @item on function."""
    @fly_out
    def sample_func(page): pass

    assert getattr(sample_func, "_fletfly_fly_out", None)["func"] == "fly_out"
    assert getattr(sample_func, "_fletfly_fly_out", None)["inheritable"] == False
    assert getattr(sample_func, "_fletfly_fly_out", None)["apply_per_view"] == False
def test_fly_out_decorator_with_args_on_function():
    """Case c_func: @item(arg, arg) on function."""
    @fly_out(inheritable=True, role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_fly_out", None)["func"] == "fly_out"
    assert getattr(sample_func, "_fletfly_fly_out", None)["inheritable"] == True
    assert getattr(sample_func, "_fletfly_fly_out", None)["apply_per_view"] == False
    assert getattr(sample_func, "_fletfly_fly_out", None)["kwargs"]["role"] == "user"
def test_fly_out_via_class_attribute_on_function():
    """Case d_func: @Airway.item on function."""
    @Airway.fly_out
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_fly_out", None)["func"] == "fly_out"
    assert getattr(sample_func, "_fletfly_fly_out", None)["inheritable"] == False
    assert getattr(sample_func, "_fletfly_fly_out", None)["apply_per_view"] == False

def test_fly_out_via_class_attribute_with_args_on_function():
    """Case e_func: @Airway.fly_out(arg, arg) on function."""
    @Airway.fly_out(inheritable=True, role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_fly_out", None)["func"] == "fly_out"
    assert getattr(sample_func, "_fletfly_fly_out", None)["inheritable"] == True
    assert getattr(sample_func, "_fletfly_fly_out", None)["kwargs"]["role"] == "user"
    assert getattr(sample_func, "_fletfly_fly_out", None)["kwargs"].get("inheritable", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_inheritable", "not there") == "not there"

def test_fly_out_via_instance_attribute_on_function():
    """Case f_func: @Airway().item on function."""
    aw = Airway()
    @aw.fly_out
    def sample_func(page): pass
    assert sample_func in aw.fly_outs

def test_fly_out_via_instance_attribute_with_args_on_function():
    """Case g_func: @Airway().item() on function."""
    aw = Airway()
    @aw.fly_out(inheritable=True, role="user")
    def sample_func(page): pass
    assert sample_func in aw.fly_outs
    assert getattr(sample_func, "_fletfly_fly_out", None)["func"] == "fly_out"
    assert getattr(sample_func, "_fletfly_fly_out", None)["inheritable"] == True
    assert getattr(sample_func, "_fletfly_fly_out", None)["kwargs"]["role"] == "user"
    assert getattr(sample_func, "_fletfly_fly_out", None)["kwargs"].get("inheritable", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_inheritable", "not there") == "not there"