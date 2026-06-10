# fletfly/tests/routes/test_route_unify_children.py
import pytest
from fletfly import Route, General

def dummy_view(page):
    pass

def test_recursive_route_attribute_detection():
    # Scenario: Verify that the engine deeply scans Route instances attached 
    # as attributes and recursively discovers the entire hierarchy.
    
    level_three = Route(path="level-three", _view=dummy_view)
    
    level_two = Route(path="level-two", _view=dummy_view)
    level_two.child = level_three
    
    level_one = Route(path="level-one", _view=dummy_view)
    level_one.child = level_two

    Route._create_tree(handed_classes=[level_one])

    assert "/level-one" in General._tree_map
    assert "/level-one/level-two" in General._tree_map
    assert "/level-one/level-two/level-three" in General._tree_map

def test_mixed_attributes_and_children_list():
    # Scenario: Cleanly combines direct Route instance attributes 
    # and multiple routes defined within the 'children' list.
    component_a = Route(path="a")
    component_b = Route(path="b")
    component_c = Route(path="c")

    mixed_parent = Route(path="mixed")
    mixed_parent.children = [component_c]
    mixed_parent.child = component_a
    mixed_parent.child = component_b


    Route._create_tree(handed_classes=[mixed_parent])

    assert "/mixed/a" in General._tree_map
    assert "/mixed/b" in General._tree_map
    assert "/mixed/c" in General._tree_map