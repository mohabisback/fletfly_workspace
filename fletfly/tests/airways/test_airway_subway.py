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


def test_03():
    """ @route_obj.subway("/route") with explicit positional path string. """
    route_obj = Airway(path="/")
    
    @route_obj.subway("/dashboard")
    class DashboardSubway:
        build = dummy_build

    assert getattr(DashboardSubway, "path", None) == "/dashboard"
    assert getattr(DashboardSubway, "path_clsattr", None) == "path"


def test_04():
    """ @route_obj.subway(path="/route") with explicit keyword path string. """
    route_obj = Airway(path="/")
    
    @route_obj.subway(path="/analytics")
    class AnalyticsSubway:
        build = dummy_build

    assert getattr(AnalyticsSubway, "path", None) == "/analytics"
    assert getattr(AnalyticsSubway, "path_clsattr", None) == "path"


def test_05():
    """ Verify path is preserved for runtime recording with instance decorator. """
    route_obj = Airway(path="/")
    
    @route_obj.subway("/settings")
    class SettingsSubway:
        build = dummy_build

    assert hasattr(SettingsSubway, "path")
    assert SettingsSubway.path == "/settings"
    assert hasattr(SettingsSubway, "path_clsattr")
    assert SettingsSubway.path_clsattr == "path"


def test_06():
    """ Ensure '_fletfly_subway' flag is set via instance decorator. """
    route_obj = Airway(path="/")
    
    @route_obj.subway("/profile")
    class ProfileSubway:
        build = dummy_build

    assert getattr(ProfileSubway, "_fletfly_subway", None) is True


def test_subway_decorator_syntax_and_attr_recording():
    route_obj = Airway(path="/")
    
    @route_obj.subway("/billing")
    class BillingSubway:
        build = dummy_build

    assert getattr(BillingSubway, "path", None) == "/billing"
    assert getattr(BillingSubway, "path_clsattr", None) == "path"

    @route_obj.subway(path="/invoice")
    class InvoiceSubway:
        build = dummy_build

    assert getattr(InvoiceSubway, "path", None) == "/invoice"
    assert getattr(InvoiceSubway, "path_clsattr", None) == "path"

    assert getattr(BillingSubway, "_fletfly_subway", None) is True
    assert getattr(InvoiceSubway, "_fletfly_subway", None) is True


# --- Scenario 2: Auto-Path Naming Interaction ---

def test_subway_fallback_and_auto_naming():
    Airline.auto_path_naming = True
    route_obj = Airway(path="/")

    @route_obj.subway
    class User_Management_Hub:
        build = dummy_build

    @route_obj.subway()
    class Secret_Admin_Gate:
        build = dummy_build

    airway_1, _ = Airway._airway_from_class(User_Management_Hub)
    airway_2, _ = Airway._airway_from_class(Secret_Admin_Gate)

    assert airway_1.path == "user-management-hub"
    assert airway_2.path == "secret-admin-gate"


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
    customer_portal = Airway(path="customer", _build=dummy_build)
    enterprise_portal = Airway(path="enterprise", _build=dummy_build)

    @customer_portal.subway("/profile-view")
    class SharedProfileSubway:
        build = dummy_build

    # ربط نفس الـ subway بالكائن الأب الثاني أيضاً
    enterprise_portal.subways.append(SharedProfileSubway)

    Airway._map = {}
    Airway._create_tree(handed_classes=[customer_portal, enterprise_portal])

    assert "/customer/profile-view" in Airway._map
    assert "/enterprise/profile-view" in Airway._map
    assert SharedProfileSubway.path == "/profile-view"
    assert SharedProfileSubway.path_clsattr == "path"


# --- Scenario 5: Runtime Attr Recheck Preservation Simulation ---

def test_subway_runtime_attr_loop_integrity():
    route_obj = Airway(path="/")
    
    @route_obj.subway(path="/dynamic-endpoint")
    class RuntimeTargetSubway:
        build = dummy_build

    recorded_attr_name = getattr(RuntimeTargetSubway, "path_clsattr", None)
    assert recorded_attr_name == "path"
    
    runtime_resolved_value = getattr(RuntimeTargetSubway, recorded_attr_name, None)
    assert runtime_resolved_value == "/dynamic-endpoint"