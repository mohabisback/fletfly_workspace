import pytest
from fletfly import Airway

def test_vampire_successful_merge():
    """Verify that _vampire correctly merges properties without conflicts."""
    base_airway = Airway(path="home")
    victim_airway = Airway(path="home")
    
    def dummy_build(page): pass
    victim_airway._build = dummy_build
    
    merged = base_airway._vampire(victim_airway)
    assert merged._build == dummy_build
    assert len(victim_airway.__dict__) == 0

def test_vampire_conflict_raises_error():
    """Verify that _vampire raises a ValueError upon a build collision."""
    def build_one(page): pass
    def build_two(page): pass
    
    airway1 = Airway(path="profile", build=build_one)
    airway2 = Airway(path="profile", build=build_two)
    
    with pytest.raises(ValueError, match="Conflict in 'build'"):
        airway1._vampire(airway2)

def test_inject_into_tree_root():
    """Verify core injection mechanics for the root path."""
    root_node = Airway(path="")
    def root_build(page): pass
    root_node._build = root_build
    
    inserted = Airway._inject_into_tree(root_node)
    assert Airway._map.get("") is inserted