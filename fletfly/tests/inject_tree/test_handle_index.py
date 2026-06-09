# fletfly/tests/inject_tree/test_handle_index.py
import pytest
from fletfly import Airway

class DummyClass1: pass
class DummyClass2: pass

def dummy_build1(page): pass
def dummy_build2(page): pass


def test_01():
    # Should raise ValueError if parent path is None
    parent = Airway(path=None)
    child = Airway(path="", build=dummy_build2)
    with pytest.raises(ValueError, match="Can't add index with path = '' into a pathless parent route"):
        Airway._handle_index(parent, child, subways=[])


def test_02():
    # Should raise ValueError if parent already has _build set
    parent = Airway(path="/dashboard")
    parent._build = dummy_build1
    child = Airway(path="", build=dummy_build2)
    
    with pytest.raises(ValueError, match="Parent already has a view build"):
        Airway._handle_index(parent, child, subways=[])

    # Should raise ValueError if parent already has both class and build_clsattr
    parent_cls = Airway(path="/dashboard")
    parent_cls._class = DummyClass1
    parent_cls.build_clsattr = "parent_attr"
    
    child_cls = Airway(path="", build=dummy_build2)
    with pytest.raises(ValueError, match="Parent already has a view build"):
        Airway._handle_index(parent_cls, child_cls, subways=[])


def test_03():
    # Should raise ValueError if parent already has an index assigned (Duplicate check)
    parent = Airway(path="/dashboard")
    child1 = Airway(path="", build=dummy_build1)
    child2 = Airway(path="", build=dummy_build2)
    
    # First assignment succeeds
    Airway._handle_index(parent, child1, subways=[])
    
    # Second assignment must fail
    with pytest.raises(ValueError, match="already has an index"):
        Airway._handle_index(parent, child2, subways=[])


def test_04():
    # Should successfully assign child to parent.index and return True (No diffusion)
    parent = Airway(path="/dashboard")
    child = Airway(path="", build=dummy_build2)
    child.icon = "dashboard_icon"
    child.title = "Dashboard Title"

    result = Airway._handle_index(parent, child, subways=[])

    assert result is True
    assert parent._index is child
    # Core check: Attributes must NOT diffuse to the parent anymore
    assert getattr(parent, "icon", None) != "dashboard_icon"
    assert getattr(parent, "title", None) != "Dashboard Title"


def test_05():
    # Should successfully assign a CBV child to parent.index without class restriction
    parent = Airway(path="/dashboard")
    parent._class = DummyClass1

    child = Airway(path="")
    child._class = DummyClass2  # Distinct classes are now allowed
    child.build_clsattr = "custom_class_build"

    result = Airway._handle_index(parent, child, subways=[])

    assert result is True
    assert parent._index is child


def test_06(capsys):
    # Should trigger warning if index child has subroutes (subways is not empty)
    parent = Airway(path="/dashboard")
    child = Airway(path="", build=dummy_build2)
    fake_subways = ["some_subway_route"]


    with pytest.raises(ValueError):
        Airway._handle_index(parent, child, subways=fake_subways)
    

def test_07():
    # Should raise ValueError if child has neither _build nor class build indicators
    parent = Airway(path="/dashboard")
    child = Airway(path="")
    
    with pytest.raises(ValueError, match="must have a build view"):
        Airway._handle_index(parent, child, subways=[])