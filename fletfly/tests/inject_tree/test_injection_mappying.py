# test_injection_mapping.py
import pytest
from fletfly import Airway

def dummy_build(page):
    pass

def test_01():
    # Scenario: Injecting a deep real node creates placeholders.
    # Later, injecting a real node for that placeholder path must absorb its subways and fix the parent's list.
    
    # 1. Create a deep path to force placeholders at '/admin'
    deep_node = Airway(path="settings")
    Airway._inject_into_tree(deep_node, parent_full_path="admin")
    
    placeholder_admin = Airway._map["/admin"]
    assert placeholder_admin.is_placeholder is True
    assert len(placeholder_admin.subways) == 1
    assert placeholder_admin.subways[0] is deep_node

    # 2. Inject a real Airway at '/admin'
    real_admin = Airway(path="admin")
    real_admin.build = dummy_build
    
    result = Airway._inject_into_tree(real_admin)
    
    # Assertions
    assert result is real_admin
    assert Airway._map["/admin"] is real_admin
    assert getattr(Airway._map["/admin"], "is_placeholder", None) is None
    
    # The real node must have inherited the deep_node from the placeholder
    assert deep_node in real_admin.subways
    
    # The root node (parent of /admin) must now point to real_admin instead of placeholder_admin
    root_node = Airway._map[""]
    assert placeholder_admin not in root_node.subways
    assert real_admin in root_node.subways


def test_02():
    # Scenario: Injecting a path creates a root placeholder. 
    # Injecting a real root node (path="" or "/") should override it and preserve subways.
    child_node = Airway(path="dashboard")
    Airway._inject_into_tree(child_node)
    
    root_placeholder = Airway._map[""]
    assert root_placeholder.is_placeholder is True
    assert child_node in root_placeholder.subways
    
    # Inject real root
    real_root = Airway(path="")
    real_root.build = dummy_build
    
    result = Airway._inject_into_tree(real_root)
    
    assert result is real_root
    assert Airway._map[""] is real_root
    assert getattr(Airway._map[""], "is_placeholder", None) is None
    assert child_node in real_root.subways


def test_03():
    # Scenario: Attempting to inject a real path that is already occupied by another real node
    first_node = Airway(path="profile")
    Airway._inject_into_tree(first_node)
    
    second_node = Airway(path="profile")
    
    with pytest.raises(ValueError) as exc_info:
        Airway._inject_into_tree(second_node)
        
    assert "already defined" in str(exc_info.value)


def test_04():
    # Scenario: Attempting to inject a real root when a real root already exists
    first_root = Airway(path="")
    Airway._inject_into_tree(first_root)
    
    second_root = Airway(path="/")
    
    with pytest.raises(ValueError) as exc_info:
        Airway._inject_into_tree(second_root)
        
    assert "Router already has a root" in str(exc_info.value)


def test_05():
    # Scenario: Injecting a node with path=None or path="" without a parent context to adopt it
    pathless_node = Airway(path=None)
    
    with pytest.raises(ValueError) as exc_info:
        Airway._inject_into_tree(pathless_node, parent_full_path="", parent=None)
        
    assert "can't inject pathless airway into the tree" in str(exc_info.value)