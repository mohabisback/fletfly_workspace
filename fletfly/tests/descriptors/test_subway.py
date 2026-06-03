# fletfly/tests/descriptors/test_subway.py
import pytest
from fletfly import Airline, Airway, subway

class DummyParent(Airway):
    path = "dummy"
def dummy_build(page):
    pass

# --- Class Decoration Cases ---
def test_02():
    """ @subway() on class with parents. """
    @subway(parents=[DummyParent])
    class SampleSubway:
        build = dummy_build

    assert hasattr(SampleSubway, "build")


def test_03():
    """ @subway("/route") with explicit positional path string and parents. """
    @subway("/dashboard", parents=[DummyParent])
    class DashboardSubway:
        build = dummy_build

    assert getattr(DashboardSubway, "path", None) == "/dashboard"
    assert getattr(DashboardSubway, "path_clsattr", None) == "path"


def test_04():
    """ @subway(path="/route") with explicit keyword path string and parents. """
    @subway(path="/analytics", parents=[DummyParent])
    class AnalyticsSubway:
        build = dummy_build

    assert getattr(AnalyticsSubway, "path", None) == "/analytics"
    assert getattr(AnalyticsSubway, "path_clsattr", None) == "path"


def test_05():
    """ Verify path is not deleted from config and is preserved for runtime recording. """
    @subway("/settings", parents=[DummyParent])
    class SettingsSubway:
        build = dummy_build

    assert hasattr(SettingsSubway, "path")
    assert SettingsSubway.path == "/settings"
    assert hasattr(SettingsSubway, "path_clsattr")
    assert SettingsSubway.path_clsattr == "path"


def test_06():
    """ Ensure no '_fletfly_subway' flag is explicitly set or required. """
    @subway("/profile", parents=[DummyParent])
    class ProfileSubway:
        build = dummy_build
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

def test_subway_decorator_syntax_and_attr_recording():
    # 1. Positional argument
    @subway("/billing", parents=[DummyParent])
    class BillingSubway:
        build = dummy_build

    assert getattr(BillingSubway, "path", None) == "/billing"
    assert getattr(BillingSubway, "path_clsattr", None) == "path"

    # 2. Keyword argument
    @subway(path="/invoice", parents=[DummyParent])
    class InvoiceSubway:
        build = dummy_build

    assert getattr(InvoiceSubway, "path", None) == "/invoice"
    assert getattr(InvoiceSubway, "path_clsattr", None) == "path"

    # 3. No flag isolation constraint
    assert getattr(BillingSubway, "_fletfly_subway", None) is True
    assert getattr(InvoiceSubway, "_fletfly_subway", None) is True


def test_subway_fallback_and_auto_naming():
    Airline.auto_path_naming = True

    @subway(parents=[DummyParent])
    class User_Management_Hub:
        build = dummy_build

    @subway(parents=[DummyParent])
    class Secret_Admin_Gate:
        build = dummy_build

    airway_1, _ = Airway._airway_from_class(User_Management_Hub)
    airway_2, _ = Airway._airway_from_class(Secret_Admin_Gate)

    assert airway_1.path == "user-management-hub"
    assert airway_2.path == "secret-admin-gate"

    def test_subway_integration_in_parent_tree_consolidation():
        class MainDashboard(Airway):
            path = "dashboard"
            build = dummy_build

        @subway("/security-gate", parents=[MainDashboard])
        class SecuritySubway:
            build = dummy_build

        MainDashboard.Guard = SecuritySubway

        Airway._create_tree(handed_classes=[MainDashboard])

        assert "/dashboard" in Airway._map
        assert "/dashboard/security-gate" in Airway._map
        assert "/security-gate" not in Airway._map


def test_subway_multi_parent_routing_resolution():
    class CustomerPortal(Airway):
        path = "customer"
        build = dummy_build

    class EnterprisePortal(Airway):
        path = "enterprise"
        build = dummy_build

    @subway("/profile-view", parents=[CustomerPortal, EnterprisePortal])
    class SharedProfileSubway:
        build = dummy_build

    CustomerPortal.Profile = SharedProfileSubway
    EnterprisePortal.subways = [SharedProfileSubway]

    Airway._create_tree(handed_classes=[CustomerPortal, EnterprisePortal])

    assert "/customer/profile-view" in Airway._map
    assert "/enterprise/profile-view" in Airway._map
    assert SharedProfileSubway.path == "/profile-view"
    assert SharedProfileSubway.path_clsattr == "path"

    def test_subway_runtime_attr_loop_integrity():
        @subway(path="/dynamic-endpoint", parents=[DummyParent])
        class RuntimeTargetSubway:
            build = dummy_build

        recorded_attr_name = getattr(RuntimeTargetSubway, "path_clsattr", None)
        assert recorded_attr_name == "path"
        
        runtime_resolved_value = getattr(RuntimeTargetSubway, recorded_attr_name, None)
        assert runtime_resolved_value == "/dynamic-endpoint"