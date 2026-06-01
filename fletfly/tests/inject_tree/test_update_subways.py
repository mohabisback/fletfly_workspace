# fletfly/tests/inject_tree/test_update_subways.py
import pytest
from fletfly import Airway

def dummy_build(page): pass
def dummy_build_alt(page): pass

def test_update_tree_subways_single_unique_addition():
    """Verify that a single unique Airway is added to the subways list and returned directly."""
    subways_list = []
    new_airway = Airway(path="profile", build=dummy_build)
    
    result = Airway._update_tree_subways(subways_list, new_airway)
    
    assert result is new_airway
    assert len(subways_list) == 1
    assert subways_list[0] is new_airway

def test_update_tree_subways_list_unique_addition():
    """Verify that a list of unique Airway objects are all added to subways and returned as a list."""
    subways_list = []
    airway1 = Airway(path="profile", build=dummy_build)
    airway2 = Airway(path="settings", build=dummy_build)
    
    result = Airway._update_tree_subways(subways_list, [airway1, airway2])
    
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] is airway1
    assert result[1] is airway2
    assert len(subways_list) == 2

def test_update_tree_subways_exact_duplicate_ignored():
    """Verify that if an identical node exists, it is not duplicated in subways and the existing node is returned."""
    existing_brother = Airway(path="dashboard", build=dummy_build)
    subways_list = [existing_brother]
    
    duplicate_airway = Airway(path="dashboard", build=dummy_build)
    
    result = Airway._update_tree_subways(subways_list, duplicate_airway)
    
    # Must return the existing brother instance, and not expand the list length
    assert result is existing_brother
    assert len(subways_list) == 1

def test_update_tree_subways_path_match_build_conflict():
    """Verify that if paths match but configuration details differ, it raises a configuration ValueError."""
    existing_brother = Airway(path="dashboard", build=dummy_build)
    subways_list = [existing_brother]
    
    conflicting_airway = Airway(path="dashboard", build=dummy_build_alt)
    
    with pytest.raises(ValueError, match=r"\[fletfly\] Airway route with path='dashboard' already exists\."):
        Airway._update_tree_subways(subways_list, conflicting_airway)

def test_update_tree_subways_dynamic_sibling_clash():
    """Verify that adding a dynamic sub-route when one already exists at the same level raises a ValueError."""
    # Test collision with different supported dynamic styles: :, {}, []
    existing_colon = Airway(path=":id", build=dummy_build)
    subways_list = [existing_colon]
    
    conflicting_bracket = Airway(path="[user_id]", build=dummy_build)
    conflicting_brace = Airway(path="{slug}", build=dummy_build)
    
    with pytest.raises(ValueError, match="Parent route already has a dynamic sub-route"):
        Airway._update_tree_subways(subways_list, conflicting_bracket)
        
    with pytest.raises(ValueError, match="Parent route already has a dynamic sub-route"):
        Airway._update_tree_subways(subways_list, conflicting_brace)