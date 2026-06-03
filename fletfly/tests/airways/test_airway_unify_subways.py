# fletfly/tests/airways/test_airway_unify_subways.py
import pytest
from fletfly import Airway

def dummy_build(page):
    pass

def test_recursive_airway_attribute_detection():
    # Scenario: Verify that the engine deeply scans Airway instances attached 
    # as attributes and recursively discovers the entire hierarchy.
    
    level_three = Airway(path="level-three", _build=dummy_build)
    
    level_two = Airway(path="level-two", _build=dummy_build)
    level_two.subway = level_three
    
    level_one = Airway(path="level-one", _build=dummy_build)
    level_one.subway = level_two

    Airway._create_tree(handed_classes=[level_one])

    assert "/level-one" in Airway._map
    assert "/level-one/level-two" in Airway._map
    assert "/level-one/level-two/level-three" in Airway._map

def test_invalid_subways_list_type_ignored():
    # Scenario: If 'subways' attribute is not a list or tuple, 
    # the engine should ignore it safely without throwing exceptions.
    invalid_airway = Airway(path="invalid-alias", _build=dummy_build)
    invalid_airway.subways = "not-a-list-or-tuple"

    # Should execute smoothly without errors
    Airway._create_tree(handed_classes=[invalid_airway])
    
    assert "/invalid-alias" in Airway._map
    assert len(invalid_airway.subways) == 0


def test_mixed_attributes_and_subways_list():
    # Scenario: Cleanly combines direct Airway instance attributes 
    # and multiple airways defined within the 'subways' list.
    component_a = Airway(path="a")
    component_b = Airway(path="b")
    component_c = Airway(path="c")

    mixed_parent = Airway(path="mixed")
    mixed_parent.subways = [component_c]
    mixed_parent.subway = component_a
    mixed_parent.subway = component_b


    Airway._create_tree(handed_classes=[mixed_parent])

    assert "/mixed/a" in Airway._map
    assert "/mixed/b" in Airway._map
    assert "/mixed/c" in Airway._map