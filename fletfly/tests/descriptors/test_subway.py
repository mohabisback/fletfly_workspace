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

def test_06():
    """ Ensure no '_fletfly_subway' flag is explicitly set or required. """
    @subway("/profile", parents=[DummyParent])
    class ProfileSubway:
        build = dummy_build
    assert getattr(ProfileSubway, "_fletfly_subway", None)[0]["path"] == "/profile"

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

    EnterprisePortal.subways = [SharedProfileSubway]

    Airway._create_tree(handed_classes=[CustomerPortal, EnterprisePortal])
    for key in Airway._map:
        print(1111111111111, key)
    assert Airway._map["/customer/profile-view"]._class == Airway._map["/enterprise/profile-view"]._class
