# fletfly/tests/classes/test_classes_append.py
import pytest
from fletfly import Airway, Airline

def dummy_build(page):
    pass

def test_01():
    # Scenario 1: Extreme Multi-Parenting & Dynamic Naming Divergence
    # A single shared child class is used by Parent A (explicit path) and Parent B (auto-named).
    # The shared child itself has NO explicit path, meaning its path must be auto-derived 
    # and mounted correctly under both independent parent path environments without clashing.
    
    Airline.detect_decorated_classes = True
    Airline.detect_airway_subclasses = True
    Airline.auto_path_naming = True

    class Deep_Shared_Leaf:
        # No explicit path! Relying completely on auto-naming: "deep-shared-leaf"
        build = dummy_build

    # Parent One: Discovered via Pending Queue (Simulating @Airway)
    class Explicit_Parent_One:
        path = "custom-first-gate"
        build = dummy_build
        Child = Deep_Shared_Leaf

    Airway._pending_classes = {Explicit_Parent_One}

    # Parent Two: Discovered via Inheritance (Auto-named: "inherited-parent-two")
    class Inherited_Parent_Two(Airway):
        build = dummy_build
        Sub = Deep_Shared_Leaf

    # Execute consolidation pool
    Airway._create_tree(handed_classes=None)

    # Assertions for Scenario 1:
    # Verify both parent paths resolved correctly based on their distinct configurations
    assert "/custom-first-gate" in Airway._map
    assert "/inherited-parent-two" in Airway._map

    # Verify that the single leaf class successfully expanded its auto-generated identity 
    # under both unique parent branches simultaneously without any state leakage or overwriting
    assert "/custom-first-gate/deep-shared-leaf" in Airway._map
    assert "/inherited-parent-two/deep-shared-leaf" in Airway._map
    
    # Ensure it didn't accidentally get exposed as a top-level route
    assert "/deep-shared-leaf" not in Airway._map


def test_02():
    # Scenario 2: The "Hybrid Role" Edge Case (A Node being both a Parent and a Child)
    # Class MidNode is explicitly defined as a child inside RootNode.
    # At the exact same time, MidNode inherits from Airway, making it discoverable as a Root.
    # The system must process MidNode as a child under RootNode, but ALSO allow it to exist 
    # as a standalone Root route if it wasn't filtered, OR ensure it's locked down based on global child registration status.
    
    Airline.detect_decorated_classes = True
    Airline.detect_airway_subclasses = True
    Airline.auto_path_naming = True

    class LeafNode:
        path = "leaf"
        build = dummy_build

    # MidNode plays a dual role: Inherits from Airway (Potential Root) but is also adopted by RootNode
    @Airway
    class MidNode(Airway):
        path = "mid-node"
        build = dummy_build
        Next = LeafNode

    @Airway
    class RootNode:
        path = "root-node"
        build = dummy_build
        Child = MidNode

    # Execute consolidation
    Airway._create_tree(handed_classes=None)

    # Critical Assertions for Scenario 2:
    # 1. RootNode must exist as a primary root
    assert "/root-node" in Airway._map
    
    # 2. MidNode must be cleanly mapped as a child under RootNode, and LeafNode mapped under MidNode deeply
    assert "/root-node/mid-node" in Airway._map
    assert "/root-node/mid-node/leaf" in Airway._map

    # 3. Guard Check: Because MidNode was unified as a child of RootNode, it gets added to 
    # _registered_children_classes. Therefore, _append_classes MUST skip injecting it as a standalone root path.
    assert "/mid-node" not in Airway._map
    assert "/mid-node/leaf" not in Airway._map


def test_append_classes_duplicate_handling_with_mixed_subways_aliases():
    # Scenario 3: Mixed Duplication Vectors via Direct Attributes and Subways Alias Lists
    # A class defines a child directly as an attribute, and ALSO includes it inside a subways list alias.
    # The system must filter this intra-class duplication gracefully during unification without exploding or double injecting.
    
    Airline.detect_decorated_classes = True
    Airline.detect_airway_subclasses = True
    Airline.auto_path_naming = True

    class UltimateLeaf:
        path = "ultimate-leaf"
        build = dummy_build

    class ConfusedParent(Airway):
        path = "confused-parent"
        build = dummy_build
        
        # Duplication vector 1: Direct inner class attribute
        DirectChild = UltimateLeaf
        
        # Duplication vector 2: Inside an alias list
        subways = [UltimateLeaf]

    # Execute consolidation
    Airway._create_tree(handed_classes=None)

    # Assertions for Scenario 3:
    assert "/confused-parent" in Airway._map
    assert "/confused-parent/ultimate-leaf" in Airway._map
    
    # Ensure no crash happened, and the internal tracking list is a clean distinct set/list
    assert len(ConfusedParent._unified_subways) == 1
    assert "/ultimate-leaf" not in Airway._map

    # Final cleanup to keep the global slate clean
    Airway._pending_classes.clear()
    Airway._registered_children.clear()