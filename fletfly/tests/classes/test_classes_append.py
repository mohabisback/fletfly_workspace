# fletfly/tests/classes/test_classes_append.py
import pytest
from fletfly import Route, General, General, Router

def dummy_view(page):
    pass

def test_01():
    # Scenario 1: Extreme Multi-Parenting & Dynamic Naming Divergence
    # A single shared child class is used by Parent A (explicit path) and Parent B (auto-named).
    # The shared child itself has NO explicit path, meaning its path must be auto-derived 
    # and mounted correctly under both independent parent path environments without clashing.

    class Deep_Shared_Leaf:
        # No explicit path! Relying completely on auto-naming: "deep-shared-leaf"
        view = dummy_view

    # Parent One: Discovered via Pending Queue (Simulating @Route)
    class Explicit_Parent_One:
        path = "custom-first-gate"
        view = dummy_view
        Child = Deep_Shared_Leaf


    # Parent Two: Discovered via Inheritance (Auto-named: "inherited-parent-two")
    class Inherited_Parent_Two(Route):
        view = dummy_view
        Sub = Deep_Shared_Leaf

    # Execute consolidation pool
    Route._create_tree([Explicit_Parent_One])
    for item in General._main_zone_tree:
        print(item)
    # Assertions for Scenario 1:
    # Verify both parent paths resolved correctly based on their distinct configurations
    assert "/custom-first-gate" in General._main_zone_tree
    assert "/inherited-parent-two" in General._main_zone_tree

    # Verify that the single leaf class successfully expanded its auto-generated identity 
    # under both unique parent branches simultaneously without any state leakage or overwriting
    assert "/inherited-parent-two/deep-shared-leaf" in General._main_zone_tree
    assert "/custom-first-gate/deep-shared-leaf" in General._main_zone_tree
    
    # Ensure it didn't accidentally get exposed as a top-level route
    assert "/deep-shared-leaf" not in General._main_zone_tree


def test_02():
    # Scenario 2: The "Hybrid Role" Edge Case (A Node being both a Parent and a Child)
    # Class MidNode is explicitly defined as a child inside RootNode.
    # At the exact same time, MidNode inherits from Route, making it discoverable as a Root.
    # The system must process MidNode as a child under RootNode, but ALSO allow it to exist 
    # as a standalone Root route if it wasn't filtered, OR ensure it's locked down based on global child registration status.
    
    class LeafNode:
        path = "leaf"
        view = dummy_view

    # MidNode plays a dual role: Inherits from Route (Potential Root) but is also adopted by RootNode
    
    class MidNode(Route):
        path = "mid-node"
        view = dummy_view
        Next = LeafNode

    @Route
    class RootNode:
        path = "root-node"
        view = dummy_view
        Child = MidNode

    # Execute consolidation
    Route._create_tree(__name__)
    # Critical Assertions for Scenario 2:
    # 1. RootNode must exist as a primary root
    assert "/root-node" in General._main_zone_tree
    
    # 2. MidNode must be cleanly mapped as a child under RootNode, and LeafNode mapped under MidNode deeply
    assert "/root-node/mid-node" in General._main_zone_tree
    assert "/root-node/mid-node/leaf" in General._main_zone_tree

    # 3. Guard Check: Because MidNode was unified as a child of RootNode, it gets added to 
    # _registered_children_classes. Therefore, _append_classes MUST skip injecting it as a standalone root path.
    assert "/mid-node" not in General._main_zone_tree
    assert "/leaf" not in General._main_zone_tree


def test_append_classes_duplicate_handling_with_mixed_children_aliases():
    # Scenario 3: Mixed Duplication Vectors via Direct Attributes and Children Alias Lists
    # A class defines a child directly as an attribute, and ALSO includes it inside a children list alias.
    # The system must filter this intra-class duplication gracefully during unification without exploding or double injecting.

    class UltimateLeaf:
        path = "ultimate-leaf"
        view = dummy_view

    class ConfusedParent(Route):
        path = "confused-parent"
        view = dummy_view
        
        # Duplication vector 1: Direct inner class attribute
        DirectChild = UltimateLeaf
        
        # Duplication vector 2: Inside an alias list
        children = [UltimateLeaf]

    # Execute consolidation
    Route._create_tree(anchors=[__name__])

    # Assertions for Scenario 3:
    assert "/confused-parent" in General._main_zone_tree
    assert "/confused-parent/ultimate-leaf" in General._main_zone_tree
    
    # Ensure no crash happened, and the internal tracking list is a clean distinct set/list
    assert len(ConfusedParent._fletfly_children) == 1
    assert "/ultimate-leaf" not in General._main_zone_tree
