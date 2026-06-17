# fletfly/tests/routes/test_routes_append.py
import pytest
from fletfly import Route, General, Router

def dummy_view(page):
    pass

def test_01_route_multi_parenting():
    # Scenario 1: Extreme Multi-Parenting & Dynamic Routing with Pure Route Objects
    # A single shared child Route object is assigned to two independent parent Route objects.
    # All are discovered via the pending routes queue. The shared child must be mounted
    # under both parents correctly without being exposed as a standalone top-level root.
    
    Router.detect_created_routes = True
    Router.detect_route_subclasses = False

    # Create pure route objects (Simulating registration inside __init__)
    deep_shared_leaf = Route("deep-shared-leaf")
    parent_one = Route("custom-first-gate")
    parent_two = Route("inherited-parent-two")

    # Define children layout via object attributes
    parent_one.children = [deep_shared_leaf]
    parent_two.children = [deep_shared_leaf]

    # Force pending queue mapping for the test environment
    General._pending_routes = {parent_one, parent_two, deep_shared_leaf}

    # Execute consolidation pool
    Route._create_tree(anchors=[__name__])

    # Assertions for Scenario 1:
    # Verify both parent paths resolved correctly
    assert "/custom-first-gate" in General._main_zone_tree
    assert "/inherited-parent-two" in General._main_zone_tree

    # Verify that the single leaf object successfully expanded under both unique parent branches
    assert "/custom-first-gate/deep-shared-leaf" in General._main_zone_tree
    assert "/inherited-parent-two/deep-shared-leaf" in General._main_zone_tree
    
    # Guard Check: Ensure it didn't accidentally get leaked as a top-level route
    assert "/deep-shared-leaf" not in General._main_zone_tree


def test_02_route_hybrid_role():
    # Scenario 2: The "Hybrid Role" Edge Case for Route Objects
    # mid_node acts as a child to root_node, but is also a parent to leaf_node.
    # Since it's picked up in the pending queue, it must be filtered from being a standalone root
    # because it is already unified and registered as a child of root_node.
    
    General.detect_created_routes = True

    General._pending_routes.clear()
    General._registered_children.clear()
    if hasattr(Route, "_map"): General._main_zone_tree.clear()

    leaf_node = Route("leaf")
    mid_node = Route("mid-node")
    root_node = Route("root-node")

    mid_node.children = [leaf_node]
    root_node.children = [mid_node]

    General._pending_routes = {root_node, mid_node, leaf_node}

    # Execute consolidation
    Route._create_tree(anchors=[__name__])

    # Critical Assertions for Scenario 2:
    # 1. root_node must exist as a primary root
    assert "/root-node" in General._main_zone_tree
    
    # 2. Deep children nesting maps perfectly
    assert "/root-node/mid-node" in General._main_zone_tree
    assert "/root-node/mid-node/leaf" in General._main_zone_tree

    # 3. Guard Check: mid_node should not be injected as an independent root
    assert "/mid-node" not in General._main_zone_tree
    assert "/mid-node/leaf" not in General._main_zone_tree


def test_03_route_duplicate_handling_in_children_list():
    # Scenario 3: Intra-object Duplication Vector via Children Lists
    # An Route object includes the same child Route multiple times in its children list.
    # The system's set-based unification must deduplicate this gracefully without double injection.
    
    Router.detect_created_routes = True

    General._pending_routes.clear()
    General._registered_children.clear()
    if hasattr(Route, "_map"): General._main_zone_tree.clear()

    ultimate_leaf = Route("ultimate-leaf")
    confused_parent = Route("confused-parent")
    
    # Duplication vector: duplicate elements inside the children list
    confused_parent.children = [ultimate_leaf, ultimate_leaf]

    General._pending_routes = {confused_parent, ultimate_leaf}

    # Execute consolidation
    Route._create_tree(anchors=[__name__])

    # Assertions for Scenario 3:
    assert "/confused-parent" in General._main_zone_tree
    assert "/confused-parent/ultimate-leaf" in General._main_zone_tree
    assert "/ultimate-leaf" not in General._main_zone_tree
