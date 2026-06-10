# fletfly/tests/inject_tree/test_injection_mapping.py
import pytest
from fletfly import Route, General

def dummy_view(page):
    pass

def test_01():
    # Scenario: Injecting a deep real node creates placeholders.
    # Later, injecting a real node for that placeholder path must absorb its children and fix the parent's list.
    
    # 1. Create a deep path to force placeholders at '/admin'
    deep_node = Route(path="settings")
    Route._inject_into_tree(deep_node, parent_full_path="admin")
    
    placeholder_admin = General._tree_map["/admin"]
    assert placeholder_admin._is_placeholder is True
    assert len(placeholder_admin.children) == 1
    assert placeholder_admin.children[0] is deep_node

    # 2. Inject a real Route at '/admin'
    real_admin = Route(path="admin")
    real_admin.view = dummy_view
    
    result = Route._inject_into_tree(real_admin)
    
    # Assertions
    assert result is real_admin
    assert General._tree_map["/admin"] is real_admin
    assert getattr(General._tree_map["/admin"], "_is_placeholder", None) is None
    
    # The real node must have inherited the deep_node from the placeholder
    assert deep_node in real_admin.children
    
    # The root node (parent of /admin) must now point to real_admin instead of placeholder_admin
    root_node = General._tree_map[""]
    assert placeholder_admin not in root_node.children
    assert real_admin in root_node.children


def test_02():
    # Scenario: Injecting a path creates a root placeholder. 
    # Injecting a real root node (path="" or "/") should override it and preserve children.
    child_node = Route(path="dashboard")
    Route._inject_into_tree(child_node)
    
    root_placeholder = General._tree_map[""]
    assert root_placeholder._is_placeholder is True
    assert child_node in root_placeholder.children
    
    # Inject real root
    real_root = Route(path="")
    real_root.view = dummy_view
    
    result = Route._inject_into_tree(real_root)
    
    assert result is real_root
    assert General._tree_map[""] is real_root
    assert getattr(General._tree_map[""], "_is_placeholder", None) is None
    assert child_node in real_root.children


def test_03():
    # Scenario: Attempting to inject a real path that is already occupied by another real node
    first_node = Route(path="profile")
    Route._inject_into_tree(first_node)
    
    second_node = Route(path="profile", view=dummy_view)

    with pytest.raises(ValueError) as exc_info:
        Route._inject_into_tree(second_node)
        
    assert "already defined" in str(exc_info.value)


def test_04():
    # Scenario: Attempting to inject a real root when a real root already exists
    first_root = Route(path="")
    Route._inject_into_tree(first_root)
    
    second_root = Route(path="/")
    
    with pytest.raises(ValueError) as exc_info:
        Route._inject_into_tree(second_root)
        
    assert "Router already has a root" in str(exc_info.value)


def test_05():
    # Scenario: Injecting a node with path=None or path="" without a parent context to adopt it
    pathless_node = Route(path=None)
    
    with pytest.raises(ValueError) as exc_info:
        Route._inject_into_tree(pathless_node, parent_full_path="", parent=None)
        
    assert "can't inject pathless route into the tree" in str(exc_info.value)