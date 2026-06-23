# fletfly/tests/descriptors/test_view.py
import pytest
from fletfly import Route, General, view, _View

# --- Case a: Instance setting ---
def test_00():
    """Verify setting value on instance updates private attr while class descriptor remains intact."""
    aw = Route()
    def dummy_func(page): pass
    aw.view = dummy_func
    assert isinstance(Route.view, _View)
    assert aw._view["func"] == dummy_func

# --- Class Decoration Cases (6 Tests) ---
def test_01():
    """ @view on class. attr '_fletfly_view' = True only should be added to class"""
    @view
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_view")[0].get("view_hero", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_view")[0].get("props", "not there") == {}

def test_02():
    """ @view() on class. attr '_fletfly_view' = True only should be added to class"""
    @view()
    class SampleClass: pass
    
    assert getattr(SampleClass, "_fletfly_view")[0].get("view_hero", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_view")[0].get("props", "not there") == {}

def test_04():
    """ @Route.view on class. """
    @Route.view
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_view")[0].get("view_hero", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_view")[0].get("props", "not there") == {}
    
# --- Function Decoration Cases (6 Tests) ---
def test_10():
    """ @view on function."""
    @view
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_view")[0].get("view_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_view")[0].get("props", "not there") == {}


def test_11():
    """ @view() on function."""
    @view(role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_view")[0].get("view_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_view")[0].get("props", "not there") == {"role":"user"}

def test_12():
    """ @view(hero=True) on function."""
    @view(hero=True, role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_view")[0].get("view_hero", "not there") is True
    assert getattr(sample_func, "_fletfly_view")[0].get("props", "not there") == {"role":"user"}


def test_13():
    """ @Route.view on function."""
    @Route.view
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_view")[0].get("view_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_view")[0].get("props", "not there") == {}

def test_14():
    """ @Route.view() on function."""
    @Route.view(role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_view")[0].get("view_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_view")[0].get("props", "not there") == {"role":"user"}

def test_15():
    """ @Route.view(hero=True) on function."""
    @Route.view(hero=True, role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_view")[0].get("view_hero", "not there") is True
    assert getattr(sample_func, "_fletfly_view")[0].get("props", "not there") == {"role":"user"}

def test_16():
    """ @Route.view(hero=False) on function."""
    @Route.view(hero=False, role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_view")[0].get("view_hero", "not there") is False
    assert getattr(sample_func, "_fletfly_view")[0].get("props", "not there") == {"role":"user"}

def test_19():
    """Case g_func: @Route().view() on function."""
    def sample_func(page): pass
    aw = Route()
    aw.view(sample_func, hero=True, role="user")
    assert aw._view["func"] == sample_func
    assert aw._view["props"] == {"role":"user"}
    assert aw._view_hero == True

def test_20():
    """Case g_func: @Route().view() on function."""
    def sample_func(page): pass
    aw = Route()
    aw.view(sample_func, hero=False, role="user")
    assert aw._view["func"] == sample_func
    assert aw._view_hero == False
