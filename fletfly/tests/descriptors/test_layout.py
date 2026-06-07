# fletfly/tests/descriptors/test_layout.py
import pytest
from fletfly import Airway, layout, _Layout

# --- Case a: Instance setting ---
def test_00():
    """Verify setting value on instance updates private attr while class descriptor remains intact."""
    aw = Airway()
    def dummy_func(page): pass
    aw.layout = dummy_func
    assert isinstance(Airway.layout, _Layout)
    assert aw._layout["func"] == dummy_func

# --- Class Decoration Cases (6 Tests) ---
def test_01():
    """ @layout on class. attr '_fletfly_layout' = True only should be added to class"""
    @layout
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_hero", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_override", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_layout")[0].get("kwargs", "not there") == {}

def test_02():
    """ @layout() on class. attr '_fletfly_layout' = True only should be added to class"""
    @layout()
    class SampleClass: pass
    
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_hero", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_override", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_layout")[0].get("kwargs", "not there") == {}

def test_03():
    """ @layout(hero=True) on class """
    @layout(hero=True, override=True)
    class SampleClass: pass
    list(Airway._pending_airways)[0].init_kwargs = {}
    list(Airway._pending_airways)[0].layout_hero = True
    list(Airway._pending_airways)[0].layout_override = True

    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_hero", "not there") is True
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_override", "not there") is True
    assert getattr(SampleClass, "_fletfly_layout")[0].get("kwargs", "not there") == {}
    
def test_04():
    """ @Airway.layout on class. """
    @Airway.layout
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_hero", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_override", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_layout")[0].get("kwargs", "not there") == {}
    
def test_05():
    """ @Airway.layout() on class."""
    @Airway.layout()
    class SampleClass: pass
    list(Airway._pending_airways)[0].init_kwargs = {}
    list(Airway._pending_airways)[0].layout_hero = None
    list(Airway._pending_airways)[0].layout_override = None
    
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_hero", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_override", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_layout")[0].get("kwargs", "not there") == {}

def test_06():
    """ @Airway.layout(hero=True) on class."""
    @Airway.layout(hero=True, override=False, role="user")
    class SampleClass: pass
    list(Airway._pending_airways)[0].init_kwargs = {"role":"user"}
    list(Airway._pending_airways)[0].layout_hero = True
    list(Airway._pending_airways)[0].layout_override = False
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_hero", "not there") is True
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_override", "not there") is False
    assert getattr(SampleClass, "_fletfly_layout")[0].get("kwargs", "not there") == {"role":"user"}

def test_07():
    """ @Airway.layout(hero=False) on class."""
    @Airway.layout(hero=False, override=True, role="user")
    class SampleClass: pass
    list(Airway._pending_airways)[0].init_kwargs = {"role":"user"}
    list(Airway._pending_airways)[0].layout_hero = True
    list(Airway._pending_airways)[0].layout_override = False
    
    
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_hero", "not there") is False
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_override", "not there") is True
    assert getattr(SampleClass, "_fletfly_layout")[0].get("kwargs", "not there") == {"role":"user"}

def test_08():
    """ @Airway().layout on class -> error."""
    with pytest.raises(ValueError):
        @Airway().layout
        class SampleClass: pass

def test_09():
    """ @obj.layout() on class -> error."""
    with pytest.raises(ValueError):
        route = Airway()
        @route.layout()
        class SampleClass: pass

# --- Function Decoration Cases (6 Tests) ---
def test_10():
    """ @layout on function."""
    @layout
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_override", "not the" \
    "re") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("kwargs", "not there") == {}


def test_11():
    """ @layout() on function."""
    @layout(role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_override", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("kwargs", "not there") == {"role":"user"}

def test_12():
    """ @layout(hero=True) on function."""
    @layout(hero=True, override=True, role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_hero", "not there") is True
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_override", "not there") is True
    assert getattr(sample_func, "_fletfly_layout")[0].get("kwargs", "not there") == {"role":"user"}


def test_13():
    """ @Airway.layout on function."""
    @Airway.layout
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_override", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("kwargs", "not there") == {}
def test_14():
    """ @Airway.layout() on function."""
    @Airway.layout(role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_override", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("kwargs", "not there") == {"role":"user"}

def test_15():
    """ @Airway.layout(hero=True) on function."""
    @Airway.layout(hero=True, override=False, role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_hero", "not there") is True
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_override", "not there") is False
    assert getattr(sample_func, "_fletfly_layout")[0].get("kwargs", "not there") == {"role":"user"}
def test_16():
    """ @Airway.layout(hero=False) on function."""
    @Airway.layout(hero=False, override=True, role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_hero", "not there") is False
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_override", "not there") is True
    assert getattr(sample_func, "_fletfly_layout")[0].get("kwargs", "not there") == {"role":"user"}

def test_17():
    """ Airway().layout on function."""
    aw = Airway()
    @aw.layout
    def sample_func(page): pass
    assert aw._layout["func"] == sample_func
    assert aw.layout_hero is None
    assert aw.layout_override is None
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_override", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("kwargs", "not there") == {}

def test_18():
    """Case g_func: @Airway().layout() on function."""
    aw = Airway()
    @aw.layout()
    def sample_func(page): pass
    assert aw._layout["func"] == sample_func
    assert aw.layout_hero is None
    assert aw.layout_override is None
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_override", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("kwargs", "not there") == {}

def test_19():
    """Case g_func: @Airway().layout() on function."""
    aw = Airway()
    @aw.layout(hero=True, override=False, role="user")
    def sample_func(page): pass
    assert aw._layout["func"] == sample_func
    assert aw._layout["kwargs"] == {"role":"user"}
    assert aw.layout_hero is True
    assert aw.layout_override is False
    assert getattr(sample_func, "_fletfly_layout")[0]["layout_hero"]==True
    assert getattr(sample_func, "_fletfly_layout")[0]["layout_override"]==False
    assert getattr(sample_func, "_fletfly_layout")[0]["kwargs"]=={"role":"user"}

def test_20():
    """Case g_func: @Airway().layout() on function."""
    aw = Airway()
    @aw.layout(hero=False, override=True, role="user")
    def sample_func(page): pass
    assert aw._layout["func"] == sample_func
    assert aw.layout_hero is False
    assert aw.layout_override is True

    assert getattr(sample_func, "_fletfly_layout")[0]["layout_hero"]==False
    assert getattr(sample_func, "_fletfly_layout")[0]["layout_override"]==True
    assert getattr(sample_func, "_fletfly_layout")[0]["kwargs"]=={"role":"user"}