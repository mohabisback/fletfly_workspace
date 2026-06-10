# fletfly/tests/inject_tree/test_injection_classes.py
import pytest
from fletfly import Route, General

def dummy_view(page): pass

def test_01():
    # Scenario: Verify that _unify_class_children scans a class dict,
    # grabs inner classes, and processes lists defined inside aliases["children_alias"].
    
    class ChildOne:
        path = "child-one"
        _view = dummy_view

    class ChildTwo:
        path = "child-two"
        _view = dummy_view

    class ParentClass:
        path = "parent-route"
        _view = dummy_view
        
        # 1. Defined as an inner class attribute
        InnerRoute = ChildOne
        
        # 2. Defined inside a list matching the library's children_alias configuration
        children = [ChildTwo]

    # Execute the unification logic alive
    result_children = Route._unify_class_children(ParentClass)

    # Verify that both children were successfully extracted
    assert ChildOne in result_children
    assert ChildTwo in result_children
    assert len(result_children) == 2
    
    # Ensure that the unified list is stored as a class attribute on the parent
    assert hasattr(ParentClass, "_fletfly_children")
    assert ChildOne in ParentClass._fletfly_children
    assert ChildTwo in ParentClass._fletfly_children
    
    # Ensure that they are registered in the global class cache of the library
    assert ChildOne in General._registered_children
    assert ChildTwo in General._registered_children


def test_02():
    # Scenario: Verify that if a child is mentioned multiple times, it is not duplicated.
    class UniqueChild:
        path = "unique"
        view = dummy_view

    class DuplicateParent:
        path = "duplicate-parent"
        view = dummy_view
        AttrOne = UniqueChild
        children = [UniqueChild, UniqueChild]  # Intentionally duplicating the child in the list

    result = Route._unify_class_children(DuplicateParent)
    result = list(result)
    # Internal set logic must guarantee that the list contains exactly one unique instance
    assert len(result) == 1
    assert result[0] is UniqueChild


def test_03():
    # Scenario: Passing a class to _inject_into_tree should convert it via _route_from_class,
    # map it, and recursively inject its unified class children.
    
    class LeafClass:
        path = "leaf"
        view = dummy_view
        children = []

    class RootClass:
        path = "app-root"
        view = dummy_view
        Sub = LeafClass

    # Unify the class tree first to view the internal _fletfly_children structure
    Route._unify_class_children(RootClass)

    # Inject the main class directly into the tree
    result = Route._inject_into_tree(RootClass)
    
    # Verify that the class was properly converted, mapped, and its children injected recursively
    assert result is not None
    assert "/app-root" in General._tree_map
    assert General._tree_map["/app-root"].path == "app-root"
    assert "/app-root/leaf" in General._tree_map
    assert General._tree_map["/app-root/leaf"].path == "leaf"