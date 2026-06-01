# fletfly/tests/inject_tree/test_get_parent.py
import pytest
from fletfly import Airway

def test_get_parent_with_root_or_empty_path():
    """Verify that providing a root slash or empty path returns None because there is no parent segment."""
    assert Airway._get_parent("/") is None
    assert Airway._get_parent("") is None
    assert Airway._get_parent("   ") is None

def test_get_parent_single_segment():
    """Verify that a single segment path (e.g., '/home') returns the root placeholder node."""
    parent = Airway._get_parent("/home")
    
    assert parent is not None
    assert parent.is_placeholder is True
    assert "" in Airway._map
    assert Airway._map[""] is parent

def test_get_parent_deep_path_creation():
    """Verify that a deep path creates the correct placeholder hierarchy and returns the immediate parent."""
    # For path '/admin/settings/profile', the immediate parent should be the node at '/admin/settings'
    parent = Airway._get_parent("/admin/settings/profile")
    
    assert parent is not None
    assert "" in Airway._map
    assert Airway._map[""].is_placeholder is True
    assert "/admin" in Airway._map
    assert "admin" not in Airway._map
    assert Airway._map["/admin"].is_placeholder is True
    assert "/admin/settings" in Airway._map
    assert "admin/settings" not in Airway._map
    assert Airway._map["/admin/settings"].is_placeholder is True
    
    root_node = Airway._map[""]
    admin_node = Airway._map["/admin"]
    settings_node = Airway._map["/admin/settings"]
    
    # Check tree hierarchy linkage via subways
    assert admin_node in root_node.subways
    assert settings_node in admin_node.subways
    assert parent is settings_node

def test_get_parent_path_sanitization():
    """Verify that multiple consecutive slashes and trailing spaces are sanitized correctly."""
    parent_normal = Airway._get_parent("/a/b/c")
    
    # Clear map to test clean sanitization run
    Airway._map.clear()
    
    parent_dirty = Airway._get_parent("  ///a//b/c/  ")
    
    assert "/a" in Airway._map
    assert "/a/b" in Airway._map
    assert parent_dirty.path == "b"

def test_get_parent_reuses_existing_nodes_in_map():
    """Verify that _get_parent reuses an already existing node in Airway._map instead of creating a placeholder."""
    real_admin_node = Airway(path="admin")
    Airway._map["/admin"] = real_admin_node
    
    # Trigger parent lookup for a child of admin
    parent = Airway._get_parent("/admin/dashboard")
    
    # It must return the pre-existing real node, not override it with a placeholder
    assert parent is real_admin_node
    assert getattr(parent, "is_placeholder", False) is False

def test_get_parent_reuses_existing_nodes_in_subways():
    """Verify that if a node exists in subways but not yet in _map under that specific trace, it is picked up."""
    root_node = Airway(path="", is_placeholder=True)
    existing_child = Airway(path="blog")
    root_node.subways.append(existing_child)
    
    # Manually inject only the root to trigger the subways lookup logic for 'blog'
    Airway._map[""] = root_node
    
    parent = Airway._get_parent("/blog/posts")
    
    # The loop should find 'existing_child' in root_node.subways, map it, and return it
    assert "/blog" in Airway._map
    assert Airway._map["/blog"] is existing_child
    assert parent is existing_child