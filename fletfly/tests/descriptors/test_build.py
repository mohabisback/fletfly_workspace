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
    assert aw._build == dummy_func

# --- Class Decoration Cases (6 Tests) ---
def test_01():
    """ @build on class. attr '_fletfly_build' = True only should be added to class"""
    @build
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_build", None) is True
    assert getattr(SampleClass, "build_alias", None) is None
    assert getattr(SampleClass, "_fletfly_build_hero", None) is None
    assert getattr(SampleClass, "build_hero", None) is None
    assert getattr(SampleClass, "build_hero_alias", None) is None

def test_02():
    """ @build() on class. attr '_fletfly_build' = True only should be added to class"""
    @build()
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_build", None) is True
    assert getattr(SampleClass, "build_alias", None) is None
    assert getattr(SampleClass, "_fletfly_build_hero", None) is None
    assert getattr(SampleClass, "build_hero", None) is None
    assert getattr(SampleClass, "build_hero_alias", None) is None

def test_03():
    """ @build(hero=True) on class """
    @build(hero=True)
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_build", None) is True
    assert getattr(SampleClass, "build_alias", None) is None
    assert getattr(SampleClass, "_fletfly_build_hero", None) is None
    assert getattr(SampleClass, "build_hero", None) is True
    assert getattr(SampleClass, "build_hero_alias", None) == "build_hero"

def test_04():
    """ @Airway.build on class. """
    @Airway.build
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_build", None) is True
    assert getattr(SampleClass, "build_alias", None) is None
    assert getattr(SampleClass, "_fletfly_build_hero", None) is None
    assert getattr(SampleClass, "build_hero", None) is None
    assert getattr(SampleClass, "build_hero_alias", None) is None

def test_05():
    """ @Airway.build() on class."""
    @Airway.build()
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_build", None) is True
    assert getattr(SampleClass, "build_alias", None) is None
    assert getattr(SampleClass, "_fletfly_build_hero", None) is None
    assert getattr(SampleClass, "build_hero", None) is None
    assert getattr(SampleClass, "build_hero_alias", None) is None

def test_06():
    """ @Airway.build(hero=True) on class."""
    @Airway.build(hero=True)
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_build", None) is True
    assert getattr(SampleClass, "build_alias", None) is None
    assert getattr(SampleClass, "_fletfly_build_hero", None) is None
    assert getattr(SampleClass, "build_hero", None) is True
    assert getattr(SampleClass, "build_hero_alias", None) == "build_hero"

def test_07():
    """ @Airway.build(hero=False) on class."""
    @Airway.build(hero=False)
    class SampleClass: pass
    assert getattr(SampleClass, "_fletfly_build", None) is True
    assert getattr(SampleClass, "build_alias", None) is None
    assert getattr(SampleClass, "_fletfly_build_hero", None) is None
    assert getattr(SampleClass, "build_hero", None) is False
    assert getattr(SampleClass, "build_hero_alias", None) == "build_hero"

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
    assert getattr(sample_func, "_fletfly_build", None) is True
    assert getattr(sample_func, "_fletfly_build_hero", None) is None

def test_11():
    """ @build() on function."""
    @build()
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_build", None) is True
    assert getattr(sample_func, "_fletfly_build_hero", None) is None

def test_12():
    """ @build(hero=True) on function."""
    @build(hero=True)
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_build", None) is True
    assert getattr(sample_func, "_fletfly_build_hero", None) is True

def test_13():
    """ @Airway.build on function."""
    @Airway.build
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_build", None) is True
    assert getattr(sample_func, "_fletfly_build_hero", None) is None

def test_14():
    """ @Airway.build() on function."""
    @Airway.build()
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_build", None) is True
    assert getattr(sample_func, "_fletfly_build_hero", None) is None

def test_15():
    """ @Airway.build(hero=True) on function."""
    @Airway.build(hero=True)
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_build", None) is True
    assert getattr(sample_func, "_fletfly_build_hero", None) is True

def test_16():
    """ @Airway.build(hero=False) on function."""
    @Airway.build(hero=False)
    def sample_func(page): pass
    assert getattr(sample_func, "_fletfly_build", None) is True
    assert getattr(sample_func, "_fletfly_build_hero", None) is False

def test_17():
    """ Airway().build on function."""
    aw = Airway()
    @aw.build
    def sample_func(page): pass
    assert aw._build == sample_func
    assert aw.build_hero is None

def test_18():
    """Case g_func: @Airway().build() on function."""
    aw = Airway()
    @aw.build()
    def sample_func(page): pass
    assert aw._build == sample_func
    assert aw.build_hero is None

def test_19():
    """Case g_func: @Airway().build() on function."""
    aw = Airway()
    @aw.build(hero = True)
    def sample_func(page): pass
    assert aw._build == sample_func
    assert aw.build_hero == True

def test_20():
    """Case g_func: @Airway().build() on function."""
    aw = Airway()
    @aw.build(hero = False)
    def sample_func(page): pass
    assert aw._build == sample_func
    assert aw.build_hero == False