# fletfly/tests/inject_tree/test_injection_classes.py
import pytest
from fletfly import Airway

def dummy_build(page): pass

def test_01():
    # Scenario: Verify that _unify_class_subways scans a class dict,
    # grabs inner classes, and processes lists defined inside aliases["subways_alias"].
    
    class ChildOne:
        path = "child-one"
        _build = dummy_build

    class ChildTwo:
        path = "child-two"
        _build = dummy_build

    class ParentClass:
        path = "parent-route"
        _build = dummy_build
        
        # 1. Defined as an inner class attribute
        InnerRoute = ChildOne
        
        # 2. Defined inside a list matching the library's subways_alias configuration
        subways = [ChildTwo]

    # Execute the unification logic alive
    result_subways = Airway._unify_class_subways(ParentClass)

    # Verify that both children were successfully extracted
    assert ChildOne in result_subways
    assert ChildTwo in result_subways
    assert len(result_subways) == 2
    
    # Ensure that the unified list is stored as a class attribute on the parent
    assert hasattr(ParentClass, "_fletfly_subways")
    assert ChildOne in ParentClass._fletfly_subways
    assert ChildTwo in ParentClass._fletfly_subways
    
    # Ensure that they are registered in the global class cache of the library
    assert ChildOne in Airway._registered_children
    assert ChildTwo in Airway._registered_children


def test_02():
    # Scenario: Verify that if a child is mentioned multiple times, it is not duplicated.
    class UniqueChild:
        path = "unique"
        build = dummy_build

    class DuplicateParent:
        path = "duplicate-parent"
        build = dummy_build
        AttrOne = UniqueChild
        subways = [UniqueChild, UniqueChild]  # Intentionally duplicating the child in the list

    result = Airway._unify_class_subways(DuplicateParent)
    result = list(result)
    # Internal set logic must guarantee that the list contains exactly one unique instance
    assert len(result) == 1
    assert result[0] is UniqueChild


def test_03():
    # Scenario: Passing a class to _inject_into_tree should convert it via _airway_from_class,
    # map it, and recursively inject its unified class subways.
    
    class LeafClass:
        path = "leaf"
        build = dummy_build
        subways = []

    class RootClass:
        path = "app-root"
        build = dummy_build
        Sub = LeafClass

    # Unify the class tree first to build the internal _fletfly_subways structure
    Airway._unify_class_subways(RootClass)

    # Inject the main class directly into the tree
    result = Airway._inject_into_tree(RootClass)
    
    # Verify that the class was properly converted, mapped, and its children injected recursively
    assert result is not None
    assert "/app-root" in Airway._map
    assert Airway._map["/app-root"].path == "app-root"
    assert "/app-root/leaf" in Airway._map
    assert Airway._map["/app-root/leaf"].path == "leaf"