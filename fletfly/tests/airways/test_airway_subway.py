# fletfly/tests/airways/test_airway_subway.py
import pytest
from fletfly import Airline, Airway, subway

def dummy_build(page):
    pass

# --- Scenario 1: Instance-based Subway Decoration Cases ---
def test_02():
    """ @route_obj.subway() on class with empty parenthesis. """
    route_obj = Airway(path="/")
    
    @route_obj.subway()
    class SampleSubway:
        build = dummy_build

    assert hasattr(SampleSubway, "build")

# --- Scenario 3: Tree Consolidation & Parent-Child Path Stitching ---

def test_subway_integration_in_parent_tree_consolidation():
    # استخدام كائن Airway كأب مباشرة بدلاً من كلاس يرث منه
    main_dashboard = Airway(path="dashboard", _build=dummy_build)

    @main_dashboard.subway("/security-gate")
    class SecuritySubway:
        build = dummy_build

    Airway._map = {}
    Airway._create_tree(handed_classes=[main_dashboard])

    assert "/dashboard" in Airway._map
    assert "/dashboard/security-gate" in Airway._map
    assert "/security-gate" not in Airway._map


# --- Scenario 4: Multi-Parenting Divergence with Airway Instances ---

def test_subway_multi_parent_routing_resolution():
    customer_portal = Airway(path="customer", build=dummy_build)
    enterprise_portal = Airway(path="enterprise", build=dummy_build)

    @customer_portal.subway("/profile-view")
    class SharedProfileSubway:
        build = dummy_build

    enterprise_portal.subways.append(SharedProfileSubway)

    Airway._map = {}
    Airway._create_tree(handed_classes=[customer_portal, enterprise_portal])

    assert Airway._map["/customer/profile-view"]._class == SharedProfileSubway
    assert Airway._map["/enterprise/shared-profile-subway"]._class == SharedProfileSubway


# --- Scenario 5: Runtime Attr Recheck Preservation Simulation ---

def test_subway_runtime_attr_loop_integrity():
    route_obj = Airway(path="/")
    
    class RuntimeTargetSubway:
        build = dummy_build
    route_obj.subway(RuntimeTargetSubway, path="/dynamic-endpoint")

    assert route_obj.subways[0].path == "/dynamic-endpoint"