# fletfly/tests/descriptors/test_build.py
import pytest
from fletfly import Airway, build, _Build

# --- Case a: Instance setting ---
def test_00():
    """Verify setting value on instance updates private attr while class descriptor remains intact."""
    aw = Airway()
    def dummy_func(page): pass
    aw.build = dummy_func
    assert isinstance(Airway.build, _Build)
    assert aw._build["func"] == dummy_func

# --- Class Decoration Cases (6 Tests) ---
def test_01():
    """ @build on class. attr '_fletfly_build' = True only should be added to class"""
    @build
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_build")[0].get("build_hero", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_build")[0].get("kwargs", "not there") == {}

def test_02():
    """ @build() on class. attr '_fletfly_build' = True only should be added to class"""
    @build()
    class SampleClass: pass
    
    assert getattr(SampleClass, "_fletfly_build")[0].get("build_hero", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_build")[0].get("kwargs", "not there") == {}

def test_03():
    """ @build(hero=True) on class """
    @build(hero=True)
    class SampleClass: pass
    list(Airway._pending_airways)[0].init_kwargs = {}
    list(Airway._pending_airways)[0].build_hero = True
 
    assert getattr(SampleClass, "_fletfly_build")[0].get("build_hero", "not there") is True
    assert getattr(SampleClass, "_fletfly_build")[0].get("kwargs", "not there") == {}
    
def test_04():
    """ @Airway.build on class. """
    @Airway.build
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_build")[0].get("build_hero", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_build")[0].get("kwargs", "not there") == {}
    
def test_05():
    """ @Airway.build() on class."""
    @Airway.build()
    class SampleClass: pass
    list(Airway._pending_airways)[0].init_kwargs = {}
    list(Airway._pending_airways)[0].build_hero = None
    
    assert getattr(SampleClass, "_fletfly_build")[0].get("build_hero", "not there") == "not there"
    assert getattr(SampleClass, "_fletfly_build")[0].get("kwargs", "not there") == {}

def test_06():
    """ @Airway.build(hero=True) on class."""
    @Airway.build(hero=True, role="user")
    class SampleClass: pass
    list(Airway._pending_airways)[0].init_kwargs = {"role":"user"}
    list(Airway._pending_airways)[0].build_hero = True
    assert getattr(SampleClass, "_fletfly_build")[0].get("build_hero", "not there") is True
    assert getattr(SampleClass, "_fletfly_build")[0].get("kwargs", "not there") == {"role":"user"}

def test_07():
    """ @Airway.build(hero=False) on class."""
    @Airway.build(hero=False, role="user")
    class SampleClass: pass
    list(Airway._pending_airways)[0].init_kwargs = {"role":"user"}
    list(Airway._pending_airways)[0].build_hero = True
  
    
    assert getattr(SampleClass, "_fletfly_build")[0].get("build_hero", "not there") is False
    assert getattr(SampleClass, "_fletfly_build")[0].get("kwargs", "not there") == {"role":"user"}

def test_08():
    """ @Airway().build on class -> error."""
    with pytest.raises(ValueError):
        @Airway().build
        class SampleClass: pass

def test_09():
    """ @obj.build() on class -> error."""
    with pytest.raises(ValueError):
        route = Airway()
        @route.build()
        class SampleClass: pass

# --- Function Decoration Cases (6 Tests) ---
def test_10():
    """ @build on function."""
    @build
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_build")[0].get("build_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_build")[0].get("kwargs", "not there") == {}


def test_11():
    """ @build() on function."""
    @build(role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_build")[0].get("build_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_build")[0].get("kwargs", "not there") == {"role":"user"}

def test_12():
    """ @build(hero=True) on function."""
    @build(hero=True, role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_build")[0].get("build_hero", "not there") is True
    assert getattr(sample_func, "_fletfly_build")[0].get("kwargs", "not there") == {"role":"user"}


def test_13():
    """ @Airway.build on function."""
    @Airway.build
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_build")[0].get("build_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_build")[0].get("kwargs", "not there") == {}

def test_14():
    """ @Airway.build() on function."""
    @Airway.build(role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_build")[0].get("build_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_build")[0].get("kwargs", "not there") == {"role":"user"}

def test_15():
    """ @Airway.build(hero=True) on function."""
    @Airway.build(hero=True, role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_build")[0].get("build_hero", "not there") is True
    assert getattr(sample_func, "_fletfly_build")[0].get("kwargs", "not there") == {"role":"user"}

def test_16():
    """ @Airway.build(hero=False) on function."""
    @Airway.build(hero=False, role="user")
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_build")[0].get("build_hero", "not there") is False
    assert getattr(sample_func, "_fletfly_build")[0].get("kwargs", "not there") == {"role":"user"}

def test_17():
    """ Airway().build on function."""
    aw = Airway()
    @aw.build
    def sample_func(page): pass
    assert aw._build["func"] == sample_func
    assert aw.build_hero is None
    assert getattr(sample_func, "_fletfly_build")[0].get("build_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_build")[0].get("kwargs", "not there") == {}

def test_18():
    """Case g_func: @Airway().build() on function."""
    aw = Airway()
    @aw.build()
    def sample_func(page): pass
    assert aw._build["func"] == sample_func
    assert aw.build_hero is None
    assert getattr(sample_func, "_fletfly_build")[0].get("build_hero", "not there") == "not there"
    assert getattr(sample_func, "_fletfly_build")[0].get("kwargs", "not there") == {}

def test_19():
    """Case g_func: @Airway().build() on function."""
    aw = Airway()
    @aw.build(hero=True, role="user")
    def sample_func(page): pass
    assert aw._build["func"] == sample_func
    assert aw._build["kwargs"] == {"role":"user"}
    assert aw.build_hero is True
    assert getattr(sample_func, "_fletfly_build")[0]["build_hero"]==True
    assert getattr(sample_func, "_fletfly_build")[0]["kwargs"]=={"role":"user"}

def test_20():
    """Case g_func: @Airway().build() on function."""
    aw = Airway()
    @aw.build(hero=False, role="user")
    def sample_func(page): pass
    assert aw._build["func"] == sample_func
    assert aw.build_hero is False

    assert getattr(sample_func, "_fletfly_build")[0]["build_hero"]==False
    assert getattr(sample_func, "_fletfly_build")[0]["kwargs"]=={"role":"user"}