# fletfly/tests/inject_tree/test_injection_input_and_index.py
import pytest
from fletfly import Airway

def dummy_build(page):
    pass

def dummy_build2(page):
    pass


def test_01():
    # Edge Case: Ensure that when an Airway instance is processed, its subways 
    # are extracted into a local variable and the instance's subways list is cleared immediately.
    parent_node = Airway(path="dashboard")
    child_node = Airway(path="settings")
    parent_node.subways = [child_node]

    result = Airway._inject_into_tree(parent_node)
    assert Airway._map[''].path == ""
    assert Airway._map[''].is_placeholder is True
    assert Airway._map['/dashboard'].path == "dashboard"
    assert getattr(Airway._map['/dashboard'], "is_placeholder", None) is None
    assert Airway._map['/dashboard'] == parent_node
    assert Airway._map['/dashboard/settings'].path == "settings"
    assert getattr(Airway._map['/dashboard/settings'], "is_placeholder", None) is None
    assert Airway._map['/dashboard/settings'] == child_node
    assert result is parent_node
    # The list should contain exactly the child_node once (rebuilt via recursion)
    assert len(parent_node.subways) == 1
    assert parent_node.subways[0] is child_node


def test_02():
    # Edge Case: Passing an invalid type (like None or a string) should return None safely.
    assert Airway._inject_into_tree(None) is None
    assert Airway._inject_into_tree("not_an_airway_instance") is None


def test_03():
    # Test basic path combination and leading slash enforcement
    airway = Airway(path="profile")
    Airway._inject_into_tree(airway, parent_full_path="user")
    
    # "user" + "/" + "profile" -> "user/profile" -> stripped -> "/user/profile"
    assert "/user/profile" in Airway._map
    assert Airway._map["/user/profile"] is airway
    assert airway.path == "profile"

def test_04():
    # Test single path with many far nodes
    airway = Airway(path="/a/b/c/")
    Airway._inject_into_tree(airway)
    
    assert "" in Airway._map
    assert Airway._map["/a"].path == "a"
    assert Airway._map["/a"].is_placeholder is True
    assert Airway._map["/a/b"].path == "b"
    assert Airway._map["/a/b"].is_placeholder is True
    assert Airway._map["/a/b/c"].path == "c"
    assert Airway._map["/a/b/c"] == airway
    assert getattr(Airway._map["/a/b/c"], "is_placeholder", None) is None


def test_05():
    # Test single path with many far nodes
    airway = Airway(path="//c///d//")
    Airway._inject_into_tree(airway, parent_full_path="//a/b///")
    print(Airway._map)
    assert "" in Airway._map
    assert Airway._map["/a"].path == "a"
    assert Airway._map["/a"].is_placeholder is True
    assert Airway._map["/a/b"].path == "b"
    assert Airway._map["/a/b"].is_placeholder is True
    assert Airway._map["/a/b/c"].path == "c"
    assert Airway._map["/a/b/c"].is_placeholder is True
    assert Airway._map["/a/b/c/d"].path == "d"
    assert Airway._map["/a/b/c/d"] == airway
    assert getattr(Airway._map["/a/b/c/d"], "is_placeholder", None) is None


def test_inject_handle_index_early_return_alive():
    # Edge Case: Trigger Airway._handle_index naturally to verify the early return logic.
    # To succeed: parent.path is not None, child.path == "", parent has no build, child has _build.
    parent = Airway(path="dashboard")
    child = Airway(path="")
    child._build = dummy_build2

    # Clear maps to ensure a clean testing environment
    if "" in Airway._map: del Airway._map[""]
    if "/" in Airway._map: del Airway._map["/"]

    # Invoke injection with active parent context
    result = Airway._inject_into_tree(child, parent_full_path="dashboard", parent=parent)

    # It must return the child early, assigning parent.index, and NOT adding the pathless child to the map
    assert result is child
    assert "" not in Airway._map
    assert "/" not in Airway._map
    assert parent.index is child  # Verified that explicit reference assignment happened alive