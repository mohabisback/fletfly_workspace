# fletfly/tests/inject_tree/test_injection_input_and_index.py
import pytest
from fletfly import Route, General

def dummy_view(page):
    pass

def dummy_view2(page):
    pass


def test_01():
    # Edge Case: Ensure that when an Route instance is processed, its children 
    # are extracted into a local variable and the instance's children list is cleared immediately.
    parent_node = Route(path="dashboard")
    child_node = Route(path="settings")
    parent_node.children = [child_node]

    result = Route._inject_into_tree(parent_node)
    assert General._tree_map[''].path == ""
    assert General._tree_map['']._is_placeholder is True
    assert General._tree_map['/dashboard'].path == "dashboard"
    assert getattr(General._tree_map['/dashboard'], "_is_placeholder", None) is None
    assert General._tree_map['/dashboard'] == parent_node
    assert General._tree_map['/dashboard/settings'].path == "settings"
    assert getattr(General._tree_map['/dashboard/settings'], "_is_placeholder", None) is None
    assert General._tree_map['/dashboard/settings'] == child_node
    assert result is parent_node
    # The list should contain exactly the child_node once (rebuilt via recursion)
    assert len(parent_node.children) == 1
    assert parent_node.children[0] is child_node


def test_02():
    # Edge Case: Passing an invalid type (like None or a string) should return None safely.
    assert Route._inject_into_tree(None) is None
    assert Route._inject_into_tree("not_an_route_instance") is None


def test_03():
    # Test basic path combination and leading slash enforcement
    route = Route(path="profile")
    Route._inject_into_tree(route, parent_full_path="user")
    
    # "user" + "/" + "profile" -> "user/profile" -> stripped -> "/user/profile"
    assert "/user/profile" in General._tree_map
    assert General._tree_map["/user/profile"] is route
    assert route.path == "profile"

def test_04():
    # Test single path with many far nodes
    route = Route(path="/a/b/c/")
    Route._inject_into_tree(route)
    
    assert "" in General._tree_map
    assert General._tree_map["/a"].path == "a"
    assert General._tree_map["/a"]._is_placeholder is True
    assert General._tree_map["/a/b"].path == "b"
    assert General._tree_map["/a/b"]._is_placeholder is True
    assert General._tree_map["/a/b/c"].path == "c"
    assert General._tree_map["/a/b/c"] == route
    assert getattr(General._tree_map["/a/b/c"], "_is_placeholder", None) is None


def test_05():
    # Test single path with many far nodes
    route = Route(path="//c///d//")
    Route._inject_into_tree(route, parent_full_path="//a/b///")
    assert "" in General._tree_map
    assert General._tree_map["/a"].path == "a"
    assert General._tree_map["/a"]._is_placeholder is True
    assert General._tree_map["/a/b"].path == "b"
    assert General._tree_map["/a/b"]._is_placeholder is True
    assert General._tree_map["/a/b/c"].path == "c"
    assert General._tree_map["/a/b/c"]._is_placeholder is True
    assert General._tree_map["/a/b/c/d"].path == "d"
    assert General._tree_map["/a/b/c/d"] == route
    assert getattr(General._tree_map["/a/b/c/d"], "_is_placeholder", None) is None


def test_inject_handle_index_early_return_alive():
    # Edge Case: Trigger Route._handle_index naturally to verify the early return logic.
    # To succeed: parent.path is not None, child.path == "", parent has no view, child has _view.
    parent = Route(path="dashboard")
    child = Route(path="")
    child._view = dummy_view2

    # Clear maps to ensure a clean testing environment
    if "" in General._tree_map: del General._tree_map[""]
    if "/" in General._tree_map: del General._tree_map["/"]

    # Invoke injection with active parent context
    result = Route._inject_into_tree(child, parent_full_path="dashboard", parent=parent)

    # It must return the child early, assigning parent.index, and NOT adding the pathless child to the map
    assert result is child
    assert "" not in General._tree_map
    assert "/" not in General._tree_map
    assert parent._index is child  # Verified that explicit reference assignment happened alive