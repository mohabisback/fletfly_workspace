# fletfly/tests/airways/test_update_tree_subways.py
import pytest
from fletfly import Airway

def dummy_build(page):
    pass


def test_add_single_new_airway():
    subways = []
    new_airway = Airway(path="profile", _build=dummy_build)
    
    result = Airway._update_tree_subways(subways, new_airway)
    
    assert result == new_airway
    assert len(subways) == 1
    assert subways[0] == new_airway


def test_add_multiple_new_airways():
    subways = []
    airway_a = Airway(path="home", _build=dummy_build)
    airway_b = Airway(path="settings", _build=dummy_build)
    
    result = Airway._update_tree_subways(subways, [airway_a, airway_b])
    
    assert result == [airway_a, airway_b]
    assert len(subways) == 2
    assert airway_a in subways
    assert airway_b in subways


def test_static_path_collision_returns_existing_brother():
    existing_brother = Airway(path="dashboard", _build=dummy_build)
    subways = [existing_brother]
    
    duplicate_airway = Airway(path="dashboard", _build=dummy_build)
    
    result = Airway._update_tree_subways(subways, duplicate_airway)
    
    assert result == existing_brother
    assert len(subways) == 1
    assert subways[0] == existing_brother


@pytest.mark.parametrize("existing_path, new_path", [
    (":id", "{name}"),
    ("{uid}", "[category]"),
    ("[slug]", ":post_id"),
    (":param", ":another")
])
def test_dynamic_route_collision_raises_value_error(existing_path, new_path):
    existing_brother = Airway(path=existing_path, _build=dummy_build)
    subways = [existing_brother]
    
    clashing_airway = Airway(path=new_path, _build=dummy_build)
    
    with pytest.raises(ValueError, match="Parent route already has a dynamic sub-route"):
        Airway._update_tree_subways(subways, clashing_airway)


def test_mixed_static_and_dynamic_at_same_level_allowed():
    existing_static = Airway(path="static-route", _build=dummy_build)
    subways = [existing_static]
    
    dynamic_airway = Airway(path=":id", _build=dummy_build)
    
    result = Airway._update_tree_subways(subways, dynamic_airway)
    
    assert result == dynamic_airway
    assert len(subways) == 2
    assert dynamic_airway in subways


def test_mixed_list_input_handling():
    existing_brother = Airway(path="existing", _build=dummy_build)
    subways = [existing_brother]
    
    duplicate_airway = Airway(path="existing", _build=dummy_build)
    new_airway = Airway(path="new-path", _build=dummy_build)
    
    result = Airway._update_tree_subways(subways, [duplicate_airway, new_airway])
    
    assert result == [existing_brother, new_airway]
    assert len(subways) == 2
    assert new_airway in subways