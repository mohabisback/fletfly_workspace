# fletfly/tests/inject_tree/test_handle_index.py
import pytest
from fletfly import Route, General

class DummyClass1: pass
class DummyClass2: pass

def dummy_view1(page): pass
def dummy_view2(page): pass


def test_01():
    # Should raise ValueError if parent path is None
    parent = Route(path=None)
    child = Route(path="", view=dummy_view2)
    with pytest.raises(ValueError, match="Can't add index with path = '' into a pathless parent route"):
        Route._handle_index(parent, child, children=[])


def test_02():
    # Should raise ValueError if parent already has _view set
    parent = Route(path="/dashboard")
    parent._view = dummy_view1
    child = Route(path="", view=dummy_view2)
    
    with pytest.raises(ValueError, match="Parent already has a view view"):
        Route._handle_index(parent, child, children=[])

    # Should raise ValueError if parent already has both class and view_clsattr
    parent_cls = Route(path="/dashboard")
    parent_cls._class = DummyClass1
    parent_cls.view = "parent_attr"
    
    child_cls = Route(path="", view=dummy_view2)
    with pytest.raises(ValueError, match="Parent already has a view view"):
        Route._handle_index(parent_cls, child_cls, children=[])


def test_03():
    # Should raise ValueError if parent already has an index assigned (Duplicate check)
    parent = Route(path="/dashboard")
    child1 = Route(path="", view=dummy_view1)
    child2 = Route(path="", view=dummy_view2)
    
    # First assignment succeeds
    Route._handle_index(parent, child1, children=[])
    
    # Second assignment must fail
    with pytest.raises(ValueError, match="already has an index"):
        Route._handle_index(parent, child2, children=[])


def test_04():
    # Should successfully assign child to parent.index and return True (No diffusion)
    parent = Route(path="/dashboard")
    child = Route(path="", view=dummy_view2)
    child.icon = "dashboard_icon"
    child.title = "Dashboard Title"

    result = Route._handle_index(parent, child, children=[])

    assert result is True
    assert parent._index is child
    # Core check: Attributes must NOT diffuse to the parent anymore
    assert getattr(parent, "icon", None) != "dashboard_icon"
    assert getattr(parent, "title", None) != "Dashboard Title"


def test_05():
    # Should successfully assign a CBV child to parent.index without class restriction
    parent = Route(path="/dashboard")
    parent._class = DummyClass1

    child = Route(path="")
    child._class = DummyClass2  # Distinct classes are now allowed
    child.view = "custom_class_view"

    result = Route._handle_index(parent, child, children=[])

    assert result is True
    assert parent._index is child


def test_06(capsys):
    # Should trigger warning if index child has subroutes (children is not empty)
    parent = Route(path="/dashboard")
    child = Route(path="", view=dummy_view2)
    fake_children = ["some_child_route"]


    with pytest.raises(ValueError):
        Route._handle_index(parent, child, children=fake_children)
    

def test_07():
    # Should raise ValueError if child has neither _view nor class view indicators
    parent = Route(path="/dashboard")
    child = Route(path="")
    
    with pytest.raises(ValueError, match="must have a view"):
        Route._handle_index(parent, child, children=[])