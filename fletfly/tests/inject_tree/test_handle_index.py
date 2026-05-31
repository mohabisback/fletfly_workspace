# test_handle_index.py
import pytest
from fletfly import Airway

class DummyClass1: pass
class DummyClass2: pass

def dummy_build1(page): pass
def dummy_build2(page): pass


def test_01():
    # Should return False if either parent or child is missing
    assert Airway._handle_index(None, Airway(path="")) is False
    assert Airway._handle_index(Airway(path=""), None) is False


def test_02():
    # Should return False if parent path is None or "/"
    parent = Airway(path=None)
    child = Airway(path="", build = dummy_build2)
    assert Airway._handle_index(parent, child) is False
    
    # should return False if child path is None or Value
    parent = Airway(path="/dashboard")
    child = Airway(component = dummy_build2)
    assert Airway._handle_index(parent, child) is False

    parent = Airway(path="/dashboard")
    child = Airway(path="value", element = dummy_build2)
    assert Airway._handle_index(parent, child) is False


def test_03():
    # Should return False if parent already has _build set
    parent = Airway(path="/dashboard", view = dummy_build1)
    child = Airway(path="")
    child.build = dummy_build2
    assert Airway._handle_index(parent, child) is False

    # Should return False if parent already has both class and build_clsattr
    parent_cls = Airway(path="/dashboard")
    parent_cls._class = DummyClass1
    parent_cls.build_clsattr = "parent_attr"
    
    child_cls = Airway(path="")
    child_cls.view = dummy_build2
    assert Airway._handle_index(parent_cls, child_cls) is False


def test_04():
    # Should diffuse static attributes and return True when child._build exists
    parent = Airway(path="/dashboard")
    child = Airway(path="", build=dummy_build2)
    child.icon = "dashboard_icon"
    child.title = "Dashboard Title"

    result = Airway._handle_index(parent, child)

    assert result is True
    assert parent._build == dummy_build2
    assert parent.icon == "dashboard_icon"
    assert parent.title == "Dashboard Title"


def test_05():
    # Should diffuse both static and CBV attributes when classes match
    parent = Airway(path="/dashboard")
    parent._class = DummyClass1

    child = Airway(path="")
    child._class = DummyClass1
    child.build_clsattr = "custom_class_build"
    child.icon_clsattr = "custom_class_icon"
    child.title = "CBV Title"

    result = Airway._handle_index(parent, child)

    assert result is True
    assert parent.build_clsattr == "custom_class_build"
    assert parent.icon_clsattr == "custom_class_icon"
    assert parent.title == "CBV Title"


def test_06(capsys):
    # Should trigger warning and return False if parent and child have distinct classes
    parent = Airway(path="/dashboard")
    parent._class = DummyClass1

    child = Airway(path="")
    child._class = DummyClass2
    child.build_clsattr = "some_clsattr"

    result = Airway._handle_index(parent, child)

    assert result is False
    captured = capsys.readouterr()
    assert "[fletfly] WARNING:" in captured.out
    assert "destinct class <DummyClass2>" in captured.out
    assert "parent class <DummyClass1>" in captured.out


def test_07(capsys):
    # Should trigger warning specifying 'parent class-less route' if parent has no class
    parent = Airway(path="/dashboard")
    # parent._class is None

    child = Airway(path="")
    child._class = DummyClass2
    child.build_clsattr = "some_clsattr"

    result = Airway._handle_index(parent, child)

    assert result is False
    captured = capsys.readouterr()
    assert "[fletfly] WARNING:" in captured.out
    assert "destinct class <DummyClass2>" in captured.out
    assert "parent class-less route" in captured.out


def test_08():
    # Should return False if child has neither _build nor class indicators
    parent = Airway(path="/dashboard")
    child = Airway(path="")
    
    assert Airway._handle_index(parent, child) is False