# fletfly/tests/routes/test_route_child.py
import pytest
from fletfly import Router, General, Route, child

def dummy_view(page):
    pass

# --- Scenario 1: Instance-based Child Decoration Cases ---
def test_02():
    """ @route_obj.child() on class with empty parenthesis. """
    route_obj = Route(path="/")
    
    @route_obj.child()
    class SampleChild:
        view = dummy_view

    assert hasattr(SampleChild, "view")

# --- Scenario 3: Tree Consolidation & Parent-Child Path Stitching ---

def test_child_integration_in_parent_tree_consolidation():
    # استخدام كائن Route كأب مباشرة بدلاً من كلاس يرث منه
    main_dashboard = Route(path="dashboard", _view=dummy_view)

    @main_dashboard.child("/security-gate")
    class SecurityChild:
        view = dummy_view

    General._main_zone_tree = {}
    Route._create_tree(anchors=[main_dashboard])

    assert "/dashboard" in General._main_zone_tree
    assert "/dashboard/security-gate" in General._main_zone_tree
    assert "/security-gate" not in General._main_zone_tree


# --- Scenario 4: Multi-Parenting Divergence with Route Instances ---

def test_child_multi_parent_routing_resolution():
    customer_portal = Route(path="customer", view=dummy_view)
    enterprise_portal = Route(path="enterprise", view=dummy_view)

    @customer_portal.child("/profile-view")
    class SharedProfileChild:
        view = dummy_view

    enterprise_portal.children.append(SharedProfileChild)

    General._main_zone_tree = {}
    Route._create_tree(anchors=[customer_portal, enterprise_portal])

    assert General._main_zone_tree["/customer/profile-view"]._class == SharedProfileChild
    assert General._main_zone_tree["/enterprise/shared-profile-child"]._class == SharedProfileChild


# --- Scenario 5: Runtime Attr Recheck Preservation Simulation ---

def test_child_runtime_attr_loop_integrity():
    route_obj = Route(path="/")
    
    class RuntimeTargetChild:
        view = dummy_view
    route_obj.child(RuntimeTargetChild, path="/dynamic-endpoint")

    assert route_obj.children[0].path == "/dynamic-endpoint"