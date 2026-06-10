# fletfly/tests/inject_tree/test_get_parent.py
import pytest
from fletfly import Route, General, General, General

def test_get_parent_with_root_or_empty_path():
    """Verify that providing a root slash or empty path returns None because there is no parent segment."""
    assert Route._get_parent("/") is None
    assert Route._get_parent("") is None
    assert Route._get_parent("   ") is None

def test_get_parent_single_segment():
    """Verify that a single segment path (e.g., '/home') returns the root placeholder node."""
    parent = Route._get_parent("/home")
    
    assert parent is not None
    assert parent._is_placeholder is True
    assert "" in General._tree_map
    assert General._tree_map[""] is parent

def test_get_parent_deep_path_creation():
    """Verify that a deep path creates the correct placeholder hierarchy and returns the immediate parent."""
    # For path '/admin/settings/profile', the immediate parent should be the node at '/admin/settings'
    parent = Route._get_parent("/admin/settings/profile")
    
    assert parent is not None
    assert "" in General._tree_map
    assert General._tree_map[""]._is_placeholder is True
    assert "/admin" in General._tree_map
    assert "admin" not in General._tree_map
    assert General._tree_map["/admin"]._is_placeholder is True
    assert "/admin/settings" in General._tree_map
    assert "admin/settings" not in General._tree_map
    assert General._tree_map["/admin/settings"]._is_placeholder is True
    
    root_node = General._tree_map[""]
    admin_node = General._tree_map["/admin"]
    settings_node = General._tree_map["/admin/settings"]
    
    # Check tree hierarchy linkage via children
    assert admin_node in root_node.children
    assert settings_node in admin_node.children
    assert parent is settings_node

def test_get_parent_path_sanitization():
    """Verify that multiple consecutive slashes and trailing spaces are sanitized correctly."""
    parent_normal = Route._get_parent("/a/b/c")
    
    # Clear map to test clean sanitization run
    General._tree_map.clear()
    
    parent_dirty = Route._get_parent("  ///a//b/c/  ")
    
    assert "/a" in General._tree_map
    assert "/a/b" in General._tree_map
    assert parent_dirty.path == "b"

def test_get_parent_reuses_existing_nodes_in_map():
    """Verify that _get_parent reuses an already existing node in General._tree_map instead of creating a placeholder."""
    real_admin_node = Route(path="admin")
    General._tree_map["/admin"] = real_admin_node
    
    # Trigger parent lookup for a child of admin
    parent = Route._get_parent("/admin/dashboard")
    
    # It must return the pre-existing real node, not override it with a placeholder
    assert parent is real_admin_node
    assert getattr(parent, "_is_placeholder", False) is False

def test_get_parent_reuses_existing_nodes_in_children():
    """Verify that if a node exists in children but not yet in _map under that specific trace, it is picked up."""
    root_node = Route(path="", _is_placeholder=True)
    existing_child = Route(path="blog")
    root_node.children.append(existing_child)
    
    # Manually inject only the root to trigger the children lookup logic for 'blog'
    General._tree_map[""] = root_node
    
    parent = Route._get_parent("/blog/posts")
    
    # The loop should find 'existing_child' in root_node.children, map it, and return it
    assert "/blog" in General._tree_map
    assert General._tree_map["/blog"] is existing_child
    assert parent is existing_child