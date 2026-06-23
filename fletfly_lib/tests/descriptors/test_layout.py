# fletfly/tests/descriptors/test_layout.py
import pytest
from fletfly import Route, General, layout, _Layout

# --- Case a: Instance setting ---
def test_00():
    """Verify setting value on instance updates private attr while class descriptor remains intact."""
    aw = Route()
    def dummy_func(page): pass
    aw.layout = dummy_func
    assert isinstance(Route.layout, _Layout)
    assert aw._layout["func"] == dummy_func

# --- Class Decoration Cases (6 Tests) ---
def test_01():
    """ @layout on class. attr '_fletfly_layout' = True only should be added to class"""
    @layout
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_hero", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_override", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_layout")[0].get("props", "not there") == {}

def test_02():
    """ @layout() on class. attr '_fletfly_layout' = True only should be added to class"""
    @layout()
    class SampleClass: pass
    
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_hero", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_override", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_layout")[0].get("props", "not there") == {}
 
def test_04():
    """ @Route.layout on class. """
    @Route.layout
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_hero", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_layout")[0].get("layout_override", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_layout")[0].get("props", "not there") == {}
    
# --- Function Decoration Cases (6 Tests) ---
def test_10():
    """ @layout on function."""
    @layout
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_override", "not the" \
    "re") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("props", "not there") == {}


def test_11():
    """ @layout() on function."""
    @layout(role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_override", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("props", "not there") == {"role":"user"}

def test_12():
    """ @layout(hero=True) on function."""
    @layout(hero=True, override=True, role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_hero", "not there") is True
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_override", "not there") is True
    assert getattr(sample_func, "_fletfly_layout")[0].get("props", "not there") == {"role":"user"}


def test_13():
    """ @Route.layout on function."""
    @Route.layout
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_override", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("props", "not there") == {}
def test_14():
    """ @Route.layout() on function."""
    @Route.layout(role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_override", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_layout")[0].get("props", "not there") == {"role":"user"}

def test_15():
    """ @Route.layout(hero=True) on function."""
    @Route.layout(hero=True, override=False, role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_hero", "not there") is True
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_override", "not there") is False
    assert getattr(sample_func, "_fletfly_layout")[0].get("props", "not there") == {"role":"user"}
def test_16():
    """ @Route.layout(hero=False) on function."""
    @Route.layout(hero=False, override=True, role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_hero", "not there") is False
    assert getattr(sample_func, "_fletfly_layout")[0].get("layout_override", "not there") is True
    assert getattr(sample_func, "_fletfly_layout")[0].get("props", "not there") == {"role":"user"}

def test_18():
    """Case g_func: @Route().layout() on function."""
    def sample_func(page): pass
    aw = Route()
    aw.layout()
    assert aw._layout == None
    assert not aw.layout_hero
    assert not aw._layout_override

def test_19():
    """Case g_func: @Route().layout() on function."""
    def sample_func(page): pass
    aw = Route()
    aw.layout(sample_func, hero=True, override=False, role="user")
    assert aw._layout["func"] == sample_func
    assert aw._layout["props"] == {"role":"user"}
    assert aw.layout_hero
    assert not aw.layout_override

def test_20():
    """Case g_func: @Route().layout() on function."""
    def sample_func(page): pass
    aw = Route()
    aw.layout(sample_func, hero=False, override=True, role="user")
    
    assert aw._layout["func"] == sample_func
    assert aw.layout_hero == False
    assert aw.layout_override == True
