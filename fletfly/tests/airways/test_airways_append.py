# fletfly/tests/airways/test_airways_append.py
import pytest
from fletfly import Airway, Airline

def dummy_build(page):
    pass

def test_01_airway_multi_parenting():
    # Scenario 1: Extreme Multi-Parenting & Dynamic Routing with Pure Airway Objects
    # A single shared child Airway object is assigned to two independent parent Airway objects.
    # All are discovered via the pending airways queue. The shared child must be mounted
    # under both parents correctly without being exposed as a standalone top-level root.
    
    Airline.detect_path_routes = True
    Airline.detect_airway_subclasses = False

    # Create pure airway objects (Simulating registration inside __init__)
    deep_shared_leaf = Airway("deep-shared-leaf")
    parent_one = Airway("custom-first-gate")
    parent_two = Airway("inherited-parent-two")

    # Define subways layout via object attributes
    parent_one.subways = [deep_shared_leaf]
    parent_two.subways = [deep_shared_leaf]

    # Force pending queue mapping for the test environment
    Airway._pending_airways = {parent_one, parent_two, deep_shared_leaf}

    # Execute consolidation pool
    Airway._create_tree(handed_classes=None)

    # Assertions for Scenario 1:
    # Verify both parent paths resolved correctly
    assert "/custom-first-gate" in Airway._map
    assert "/inherited-parent-two" in Airway._map

    # Verify that the single leaf object successfully expanded under both unique parent branches
    assert "/custom-first-gate/deep-shared-leaf" in Airway._map
    assert "/inherited-parent-two/deep-shared-leaf" in Airway._map
    
    # Guard Check: Ensure it didn't accidentally get leaked as a top-level route
    assert "/deep-shared-leaf" not in Airway._map


def test_02_airway_hybrid_role():
    # Scenario 2: The "Hybrid Role" Edge Case for Airway Objects
    # mid_node acts as a child to root_node, but is also a parent to leaf_node.
    # Since it's picked up in the pending queue, it must be filtered from being a standalone root
    # because it is already unified and registered as a child of root_node.
    
    Airline.detect_path_routes = True

    Airway._pending_airways.clear()
    Airway._registered_children.clear()
    if hasattr(Airway, "_map"): Airway._map.clear()

    leaf_node = Airway("leaf")
    mid_node = Airway("mid-node")
    root_node = Airway("root-node")

    mid_node.subways = [leaf_node]
    root_node.subways = [mid_node]

    Airway._pending_airways = {root_node, mid_node, leaf_node}

    # Execute consolidation
    Airway._create_tree(handed_classes=None)

    # Critical Assertions for Scenario 2:
    # 1. root_node must exist as a primary root
    assert "/root-node" in Airway._map
    
    # 2. Deep children nesting maps perfectly
    assert "/root-node/mid-node" in Airway._map
    assert "/root-node/mid-node/leaf" in Airway._map

    # 3. Guard Check: mid_node should not be injected as an independent root
    assert "/mid-node" not in Airway._map
    assert "/mid-node/leaf" not in Airway._map


def test_03_airway_duplicate_handling_in_subways_list():
    # Scenario 3: Intra-object Duplication Vector via Subways Lists
    # An Airway object includes the same child Airway multiple times in its subways list.
    # The system's set-based unification must deduplicate this gracefully without double injection.
    
    Airline.detect_path_routes = True

    Airway._pending_airways.clear()
    Airway._registered_children.clear()
    if hasattr(Airway, "_map"): Airway._map.clear()

    ultimate_leaf = Airway("ultimate-leaf")
    confused_parent = Airway("confused-parent")
    
    # Duplication vector: duplicate elements inside the subways list
    confused_parent.subways = [ultimate_leaf, ultimate_leaf]

    Airway._pending_airways = {confused_parent, ultimate_leaf}

    # Execute consolidation
    Airway._create_tree(handed_classes=None)

    # Assertions for Scenario 3:
    assert "/confused-parent" in Airway._map
    assert "/confused-parent/ultimate-leaf" in Airway._map
    assert "/ultimate-leaf" not in Airway._map
