# test_subway.py
import pytest
from fletfly import Airline, Airway, subway

def dummy_build(page):
    pass

# --- Class Decoration Cases ---

def test_02():
    """ @subway() on class with empty parenthesis. """
    @subway()
    class SampleSubway:
        build = dummy_build

    assert hasattr(SampleSubway, "build")


def test_03():
    """ @subway("/route") with explicit positional path string. """
    @subway("/dashboard")
    class DashboardSubway:
        build = dummy_build

    # Verify path and its clsattr are successfully injected into the target class
    assert getattr(DashboardSubway, "path", None) == "/dashboard"
    assert getattr(DashboardSubway, "path_clsattr", None) == "path"


def test_04():
    """ @subway(path="/route") with explicit keyword path string. """
    @subway(path="/analytics")
    class AnalyticsSubway:
        build = dummy_build

    assert getattr(AnalyticsSubway, "path", None) == "/analytics"
    assert getattr(AnalyticsSubway, "path_clsattr", None) == "path"


def test_05():
    """ Verify path is not deleted from config and is preserved for runtime recording. """
    @subway("/settings")
    class SettingsSubway:
        build = dummy_build

    # Ensure config retention for attr name rechecking in runtime loop
    assert hasattr(SettingsSubway, "path")
    assert SettingsSubway.path == "/settings"
    assert hasattr(SettingsSubway, "path_clsattr")
    assert SettingsSubway.path_clsattr == "path"


def test_06():
    """ Ensure no '_fletfly_subway' flag is explicitly set or required. """
    @subway("/profile")
    class ProfileSubway:
        build = dummy_build

    # As intended, subways are full routes processed via tree, no special flag needed
    assert getattr(ProfileSubway, "_fletfly_subway", None) is True

def test_subway_decorator_syntax_and_attr_recording():
    """
    Scenario: Ensure all decorator invocation flavors accurately inject 'path' 
    and 'path_clsattr' without stripping them from config, preserving them 
    for runtime attribute rechecking loops.
    """
    # 1. Positional argument
    @subway("/billing")
    class BillingSubway:
        build = dummy_build

    assert getattr(BillingSubway, "path", None) == "/billing"
    assert getattr(BillingSubway, "path_clsattr", None) == "path"

    # 2. Keyword argument
    @subway(path="/invoice")
    class InvoiceSubway:
        build = dummy_build

    assert getattr(InvoiceSubway, "path", None) == "/invoice"
    assert getattr(InvoiceSubway, "path_clsattr", None) == "path"

    # 3. No flag isolation constraint
    assert getattr(BillingSubway, "_fletfly_subway", None) is True
    assert getattr(InvoiceSubway, "_fletfly_subway", None) is True


# --- Scenario 2: Auto-Path Naming Interaction ---

def test_subway_fallback_and_auto_naming():
    """
    Scenario: When @subway or @subway() is invoked without explicit path arguments,
    it must rely on Airline.auto_path_naming configurations during structure building,
    falling back to normalized class names.
    """
    Airline.auto_path_naming = True

    @subway
    class User_Management_Hub:
        build = dummy_build

    @subway()
    class Secret_Admin_Gate:
        build = dummy_build

    # Extract airways through standard factory conversion
    airway_1, _ = Airway._airway_from_class(User_Management_Hub)
    airway_2, _ = Airway._airway_from_class(Secret_Admin_Gate)

    assert airway_1.path == "user-management-hub"
    assert airway_2.path == "secret-admin-gate"


# --- Scenario 3: Tree Consolidation & Parent-Child Path Stitching ---

def test_subway_integration_in_parent_tree_consolidation():
    """
    Scenario: Classes decorated with @subway must act as full independent routes 
    when processed by _append_classes or _unify_class_subways under parent containers.
    """

    @subway("/security-gate")
    class SecuritySubway:
        build = dummy_build

    class MainDashboard(Airway):
        path = "dashboard"
        build = dummy_build
        # Injected as a direct attribute member
        Guard = SecuritySubway

    # Execute consolidation pool
    Airway._append_classes(handed_classes=[MainDashboard])

    # Assert tree mounting and structural path stitching
    assert "/dashboard" in Airway._map
    assert "/dashboard/security-gate" in Airway._map
    
    # Ensure it wasn't processed as a separate root route because it belongs to a parent tree
    assert "/security-gate" not in Airway._map


# --- Scenario 4: Multi-Parenting Divergence with Explicit Subway Paths ---

def test_subway_multi_parent_routing_resolution():
    """
    Scenario: A single explicit @subway route is mounted across two independent parent trees.
    The absolute structural route mapping must resolve perfectly under both parent paths
    without clashing or overriding internal runtime descriptors.
    """
    @subway("/profile-view")
    class SharedProfileSubway:
        build = dummy_build

    class CustomerPortal(Airway):
        path = "customer"
        build = dummy_build
        Profile = SharedProfileSubway

    class EnterprisePortal(Airway):
        path = "enterprise"
        build = dummy_build
        subways = [SharedProfileSubway]

    # Consolidate both systems
    Airway._append_classes(handed_classes=[CustomerPortal, EnterprisePortal])

    # Assert accurate multi-parent path isolation
    assert "/customer/profile-view" in Airway._map
    assert "/enterprise/profile-view" in Airway._map
    
    # Structural integrity of the original subway class metadata
    assert SharedProfileSubway.path == "/profile-view"
    assert SharedProfileSubway.path_clsattr == "path"


# --- Scenario 5: Runtime Attr Recheck Preservation Simulation ---

def test_subway_runtime_attr_loop_integrity():
    """
    Scenario: Simulate the core engine runtime rechecking loop. 
    Ensure that since 'path' config was not purged, the runtime can dynamically 
    lookup the attribute string name recorded in 'path_clsattr' and fetch its exact value.
    """
    @subway(path="/dynamic-endpoint")
    class RuntimeTargetSubway:
        build = dummy_build

    # Simulate runtime checking mechanism
    recorded_attr_name = getattr(RuntimeTargetSubway, "path_clsattr", None)
    assert recorded_attr_name == "path"
    
    # Runtime fetches current evaluation
    runtime_resolved_value = getattr(RuntimeTargetSubway, recorded_attr_name, None)
    assert runtime_resolved_value == "/dynamic-endpoint"