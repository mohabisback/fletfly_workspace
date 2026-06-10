# fletfly/tests/routes/test_update_tree_children.py
import pytest
from fletfly import Route, General

def dummy_view(page):
    pass


def test_add_single_new_route():
    children = []
    new_route = Route(path="profile", _view=dummy_view)
    
    result = Route._update_tree_children(children, new_route)
    
    assert result == new_route
    assert len(children) == 1
    assert children[0] == new_route


def test_add_multiple_new_routes():
    children = []
    route_a = Route(path="home", _view=dummy_view)
    route_b = Route(path="settings", _view=dummy_view)
    
    result = Route._update_tree_children(children, [route_a, route_b])
    
    assert result == [route_a, route_b]
    assert len(children) == 2
    assert route_a in children
    assert route_b in children


def test_static_path_collision_returns_existing_brother():
    existing_brother = Route(path="dashboard", _view=dummy_view)
    children = [existing_brother]
    
    duplicate_route = Route(path="dashboard", _view=dummy_view)
    
    result = Route._update_tree_children(children, duplicate_route)
    
    assert result == existing_brother
    assert len(children) == 1
    assert children[0] == existing_brother


@pytest.mark.parametrize("existing_path, new_path", [
    (":id", "{name}"),
    ("{uid}", "[category]"),
    ("[slug]", ":post_id"),
    (":param", ":another")
])
def test_dynamic_route_collision_raises_value_error(existing_path, new_path):
    existing_brother = Route(path=existing_path, _view=dummy_view)
    children = [existing_brother]
    
    clashing_route = Route(path=new_path, _view=dummy_view)
    
    with pytest.raises(ValueError, match="Parent route already has a dynamic sub-route"):
        Route._update_tree_children(children, clashing_route)


def test_mixed_static_and_dynamic_at_same_level_allowed():
    existing_static = Route(path="static-route", _view=dummy_view)
    children = [existing_static]
    
    dynamic_route = Route(path=":id", _view=dummy_view)
    
    result = Route._update_tree_children(children, dynamic_route)
    
    assert result == dynamic_route
    assert len(children) == 2
    assert dynamic_route in children


def test_mixed_list_input_handling():
    existing_brother = Route(path="existing", _view=dummy_view)
    children = [existing_brother]
    
    duplicate_route = Route(path="existing", _view=dummy_view)
    new_route = Route(path="new-path", _view=dummy_view)
    
    result = Route._update_tree_children(children, [duplicate_route, new_route])
    
    assert result == [existing_brother, new_route]
    assert len(children) == 2
    assert new_route in children