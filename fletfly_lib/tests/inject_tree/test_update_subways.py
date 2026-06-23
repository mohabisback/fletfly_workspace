# fletfly/tests/inject_tree/test_update_children.py
import pytest
from fletfly import Route, General

def dummy_view(page): pass
def dummy_view_alt(page): pass

def test_update_tree_children_single_unique_addition():
    """Verify that a single unique Route is added to the children list and returned directly."""
    children_list = []
    new_route = Route(path="profile", view=dummy_view)
    
    result = Route._update_tree_children(children_list, new_route)
    
    assert result is new_route
    assert len(children_list) == 1
    assert children_list[0] is new_route

def test_update_tree_children_list_unique_addition():
    """Verify that a list of unique Route objects are all added to children and returned as a list."""
    children_list = []
    route1 = Route(path="profile", view=dummy_view)
    route2 = Route(path="settings", view=dummy_view)
    
    result = Route._update_tree_children(children_list, [route1, route2])
    
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] is route1
    assert result[1] is route2
    assert len(children_list) == 2

def test_update_tree_children_exact_duplicate_ignored():
    """Verify that if an identical node exists, it is not duplicated in children and the existing node is returned."""
    existing_brother = Route(path="dashboard", view=dummy_view)
    children_list = [existing_brother]
    
    duplicate_route = Route(path="dashboard", view=dummy_view)
    
    result = Route._update_tree_children(children_list, duplicate_route)
    
    # Must return the existing brother instance, and not expand the list length
    assert result is existing_brother
    assert len(children_list) == 1

def test_update_tree_children_path_match_view_conflict():
    """Verify that if paths match but configuration details differ, it raises a configuration ValueError."""
    existing_brother = Route(path="dashboard", view=dummy_view)
    children_list = [existing_brother]
    
    conflicting_route = Route(path="dashboard", view=dummy_view_alt)
    
    with pytest.raises(ValueError, match=r"\[fletfly\] Route route with path='dashboard' already exists\."):
        Route._update_tree_children(children_list, conflicting_route)

def test_update_tree_children_dynamic_sibling_clash():
    """Verify that adding a dynamic sub-route when one already exists at the same level raises a ValueError."""
    # Test collision with different supported dynamic styles: :, {}, []
    existing_colon = Route(path=":id", view=dummy_view)
    children_list = [existing_colon]
    
    conflicting_bracket = Route(path="[user_id]", view=dummy_view)
    conflicting_brace = Route(path="{slug}", view=dummy_view)
    
    with pytest.raises(ValueError, match="Parent route already has a dynamic sub-route"):
        Route._update_tree_children(children_list, conflicting_bracket)
        
    with pytest.raises(ValueError, match="Parent route already has a dynamic sub-route"):
        Route._update_tree_children(children_list, conflicting_brace)