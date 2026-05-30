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
    assert aw._layout == dummy_func

# --- Class Decoration Cases (6 Tests) ---
def test_01():
    """ @layout on class. attr '_fletfly_layout' = True only should be added to class"""
    @layout
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_layout", None) is True
    assert getattr(SampleClass, "layout_alias", None) is None
    assert getattr(SampleClass, "_fletfly_layout_hero", None) is None
    assert getattr(SampleClass, "layout_hero", None) is None
    assert getattr(SampleClass, "layout_hero_alias", None) is None
    assert getattr(SampleClass, "layout_override", None) is None
    assert getattr(SampleClass, "layout_override_alias", None) is None

def test_02():
    """ @layout() on class. attr '_fletfly_layout' = True only should be added to class"""
    @layout()
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_layout", None) is True
    assert getattr(SampleClass, "layout_alias", None) is None
    assert getattr(SampleClass, "_fletfly_layout_hero", None) is None
    assert getattr(SampleClass, "layout_hero", None) is None
    assert getattr(SampleClass, "layout_hero_alias", None) is None
    assert getattr(SampleClass, "layout_override", None) is None
    assert getattr(SampleClass, "layout_override_alias", None) is None

def test_03():
    """ @layout(hero=True) on class """
    @layout(hero=True, override=True)
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_layout", None) is True
    assert getattr(SampleClass, "layout_alias", None) is None
    assert getattr(SampleClass, "_fletfly_layout_hero", None) is None
    assert getattr(SampleClass, "layout_hero", None) is True
    assert getattr(SampleClass, "layout_hero_alias", None) == "layout_hero"
    assert getattr(SampleClass, "layout_override", None) is True
    assert getattr(SampleClass, "layout_override_alias", None) == "layout_override"

def test_04():
    """ @Airway.layout on class. """
    @Airway.layout
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_layout", None) is True
    assert getattr(SampleClass, "layout_alias", None) is None
    assert getattr(SampleClass, "_fletfly_layout_hero", None) is None
    assert getattr(SampleClass, "layout_hero", None) is None
    assert getattr(SampleClass, "layout_hero_alias", None) is None
    assert getattr(SampleClass, "layout_override", None) is None
    assert getattr(SampleClass, "layout_override_alias", None) is None

def test_05():
    """ @Airway.layout() on class."""
    @Airway.layout()
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_layout", None) is True
    assert getattr(SampleClass, "layout_alias", None) is None
    assert getattr(SampleClass, "_fletfly_layout_hero", None) is None
    assert getattr(SampleClass, "layout_hero", None) is None
    assert getattr(SampleClass, "layout_hero_alias", None) is None
    assert getattr(SampleClass, "layout_override", None) is None
    assert getattr(SampleClass, "layout_override_alias", None) is None

def test_06():
    """ @Airway.layout(hero=True) on class."""
    @Airway.layout(hero=True, override=False)
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_layout", None) is True
    assert getattr(SampleClass, "layout_alias", None) is None
    assert getattr(SampleClass, "_fletfly_layout_hero", None) is None
    assert getattr(SampleClass, "layout_hero", None) is True
    assert getattr(SampleClass, "layout_hero_alias", None) == "layout_hero"
    assert getattr(SampleClass, "layout_override", None) is False
    assert getattr(SampleClass, "layout_override_alias", None) == "layout_override"

def test_07():
    """ @Airway.layout(hero=False) on class."""
    @Airway.layout(hero=False, override=True)
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_layout", None) is True
    assert getattr(SampleClass, "layout_alias", None) is None
    assert getattr(SampleClass, "_fletfly_layout_hero", None) is None
    assert getattr(SampleClass, "layout_hero", None) is False
    assert getattr(SampleClass, "layout_hero_alias", None) == "layout_hero"
    assert getattr(SampleClass, "layout_override", None) is True
    assert getattr(SampleClass, "layout_override_alias", None) == "layout_override"

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
    assert getattr(sample_func, "_fletfly_layout", None) is True
    assert getattr(sample_func, "_fletfly_layout_hero", None) is None
    assert getattr(sample_func, "_fletfly_layout_override", None) is None

def test_11():
    """ @layout() on function."""
    @layout()
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout", None) is True
    assert getattr(sample_func, "_fletfly_layout_hero", None) is None
    assert getattr(sample_func, "_fletfly_layout_override", None) is None

def test_12():
    """ @layout(hero=True) on function."""
    @layout(hero=True, override=True)
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout", None) is True
    assert getattr(sample_func, "_fletfly_layout_hero", None) is True
    assert getattr(sample_func, "_fletfly_layout_override", None) is True

def test_13():
    """ @Airway.layout on function."""
    @Airway.layout
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout", None) is True
    assert getattr(sample_func, "_fletfly_layout_hero", None) is None
    assert getattr(sample_func, "_fletfly_layout_override", None) is None

def test_14():
    """ @Airway.layout() on function."""
    @Airway.layout()
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout", None) is True
    assert getattr(sample_func, "_fletfly_layout_hero", None) is None
    assert getattr(sample_func, "_fletfly_layout_override", None) is None

def test_15():
    """ @Airway.layout(hero=True) on function."""
    @Airway.layout(hero=True, override=False)
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout", None) is True
    assert getattr(sample_func, "_fletfly_layout_hero", None) is True
    assert getattr(sample_func, "_fletfly_layout_override", None) is False

def test_16():
    """ @Airway.layout(hero=False) on function."""
    @Airway.layout(hero=False, override=True)
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout", None) is True
    assert getattr(sample_func, "_fletfly_layout_hero", None) is False
    assert getattr(sample_func, "_fletfly_layout_override", None) is True

def test_17():
    """ Airway().layout on function."""
    aw = Airway()
    @aw.layout
    def sample_func(page): pass
    assert aw._layout == sample_func
    assert aw.layout_hero is None
    assert aw.layout_override is None

def test_18():
    """Case g_func: @Airway().layout() on function."""
    aw = Airway()
    @aw.layout()
    def sample_func(page): pass
    assert aw._layout == sample_func
    assert aw.layout_hero is None
    assert aw.layout_override is None

def test_19():
    """Case g_func: @Airway().layout() on function."""
    aw = Airway()
    @aw.layout(hero=True, override=False)
    def sample_func(page): pass
    assert aw._layout == sample_func
    assert aw.layout_hero is True
    assert aw.layout_override is False

def test_20():
    """Case g_func: @Airway().layout() on function."""
    aw = Airway()
    @aw.layout(hero=False, override=True)
    def sample_func(page): pass
    assert aw._layout == sample_func
    assert aw.layout_hero is False
    assert aw.layout_override is True