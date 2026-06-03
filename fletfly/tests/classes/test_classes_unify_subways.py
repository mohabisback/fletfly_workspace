# fletfly/tests/classes/test_classes_unify_subways.py
from fletfly import Airway

def dummy_build(page):
    pass

def test_01():
    # Scenario: Verify that _unify_class_subways deeply scans inner class attributes 
    # and processes the entire tree recursively down to the leaf node.
    
    class LevelThree:
        path = "level-three"
        build = dummy_build

    class LevelTwo:
        path = "level-two"
        build = dummy_build
        Child = LevelThree  # Nested inner class attribute

    class LevelOne:
        path = "level-one"
        build = dummy_build
        Child = LevelTwo  # Outer inner class attribute

    # Run unification on the root of this class tree
    result = Airway._unify_class_subways(LevelOne)

    # Assertions for LevelOne
    assert LevelTwo in result
    assert len(result) == 1
    assert hasattr(LevelOne, "_unified_subways")
    assert LevelOne._unified_subways == [LevelTwo]

    # Assertions for recursive processing on LevelTwo
    assert hasattr(LevelTwo, "_unified_subways")
    assert LevelTwo._unified_subways == [LevelThree]

    # Assertions for recursive processing on LevelThree (Leaf node)
    assert hasattr(LevelThree, "_unified_subways")
    assert LevelThree._unified_subways == []

    # Verify global cache registration
    assert LevelTwo in Airway._registered_children
    assert LevelThree in Airway._registered_children


def test_02():
    # Scenario: Verify that fields starting with "_" are ignored, 
    # and a completely raw or empty class safely returns an empty list.
    
    class HiddenChild:
        path = "hidden"
        _build = dummy_build

    class TargetClass:
        path = "clean-route"
        _build = dummy_build
        _secret_route = HiddenChild  # Private attribute should be completely ignored

    result = Airway._unify_class_subways(TargetClass)

    assert len(result) == 0
    assert result == []
    assert TargetClass._unified_subways == []
    assert HiddenChild not in Airway._registered_children


def test_03():
    # Scenario: If an attribute matches a name in aliases["subways_alias"],
    # but its value is not a list or a tuple (e.g., a string or None), 
    # the method should ignore it safely without throwing exceptions.
    
    class InvalidAliasClass:
        path = "invalid-alias"
        _build = dummy_build
        subways = "not-a-list-or-tuple"  # Invalid type matching alias name
        sub_routes = None  # None value matching alias name

    result = Airway._unify_class_subways(InvalidAliasClass)

    assert len(result) == 0
    assert result == []
    assert InvalidAliasClass._unified_subways == []


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
        subways = [ComponentC]

    result = Airway._unify_class_subways(MixedParent)

    assert len(result) == 3
    assert ComponentA in result
    assert ComponentB in result
    assert ComponentC in result
    
    # Ensure all are stored correctly in the list attribute
    assert set(MixedParent._unified_subways) == {ComponentA, ComponentB, ComponentC}