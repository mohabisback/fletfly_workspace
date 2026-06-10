# fletfly/tests/classes/test_classes_unify_children.py
from fletfly import Route, General

def dummy_view(page):
    pass

def test_01():
    # Scenario: Verify that _unify_class_children deeply scans inner class attributes 
    # and processes the entire tree recursively down to the leaf node.
    
    class LevelThree:
        path = "level-three"
        view = dummy_view

    class LevelTwo:
        path = "level-two"
        view = dummy_view
        Child = LevelThree  # Nested inner class attribute

    class LevelOne:
        path = "level-one"
        view = dummy_view
        Child = LevelTwo  # Outer inner class attribute

    # Run unification on the root of this class tree
    result = Route._unify_class_children(LevelOne)

    # Assertions for LevelOne
    assert LevelTwo in result
    assert len(result) == 1
    assert hasattr(LevelOne, "_fletfly_children")
    assert LevelOne._fletfly_children == {LevelTwo}

    # Assertions for recursive processing on LevelTwo
    assert hasattr(LevelTwo, "_fletfly_children")
    assert LevelTwo._fletfly_children == {LevelThree}

    # Assertions for recursive processing on LevelThree (Leaf node)
    assert hasattr(LevelThree, "_fletfly_children")
    assert LevelThree._fletfly_children == set()

    # Verify global cache registration
    assert LevelTwo in General._registered_children
    assert LevelThree in General._registered_children


def test_02():
    # Scenario: Verify that fields starting with "_" are ignored, 
    # and a completely raw or empty class safely returns an empty list.
    
    class HiddenChild:
        path = "hidden"
        _view = dummy_view

    class TargetClass:
        path = "clean-route"
        _view = dummy_view
        _secret_route = HiddenChild  # Private attribute should be completely ignored

    result = Route._unify_class_children(TargetClass)

    assert len(result) == 0
    assert result == set()
    assert TargetClass._fletfly_children == set()
    assert HiddenChild not in General._registered_children


def test_04():
    # Scenario: Verify that the method cleanly combines a mix of direct inner class 
    # attributes and multiple classes defined within an alias list into a single unified list.
    
    class ComponentA:
        path = "a"

    class ComponentB:
        path = "b"

    class ComponentC:
        path = "c"

    class MixedParent:
        path = "mixed"
        
        # Direct inner class attributes
        RouteA = ComponentA
        RouteB = ComponentB
        
        # Alias list containing another class
        children = [ComponentC]

    result = Route._unify_class_children(MixedParent)

    assert len(result) == 3
    assert ComponentA in result
    assert ComponentB in result
    assert ComponentC in result
    
    # Ensure all are stored correctly in the list attribute
    assert set(MixedParent._fletfly_children) == {ComponentA, ComponentB, ComponentC}