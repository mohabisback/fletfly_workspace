# fletfly/tests/descriptors/test_child.py
import pytest
from fletfly import Router, Route, General, child

class DummyParent(Route):
    path = "dummy"
def dummy_view(page):
    pass

# --- Class Decoration Cases ---
def test_02():
    """ @child() on class with parents. """
    @child(parents=[DummyParent])
    class SampleChild:
        view = dummy_view

    assert hasattr(SampleChild, "view")

def test_06():
    """ Ensure no '_fletfly_child' flag is explicitly set or required. """
    @child("/profile", parents=[DummyParent])
    class ProfileChild:
        view = dummy_view
    assert getattr(ProfileChild, "_fletfly_child", None)[0]["path"] == "/profile"

def test_child_integration_in_parent_tree_consolidation():
    class MainDashboard(Route):
        path = "dashboard"
        view = dummy_view

    @child("/security-gate", parents=[MainDashboard])
    class SecurityChild:
        view = dummy_view


    Route._create_tree(handed_classes=[MainDashboard])

    assert "/dashboard" in General._tree_map
    assert "/dashboard/security-gate" in General._tree_map
    assert "/security-gate" not in General._tree_map


def test_child_multi_parent_routing_resolution():
    class CustomerPortal(Route):
        path = "customer"
        view = dummy_view

    class EnterprisePortal(Route):
        path = "enterprise"
        view = dummy_view

    @child("/profile-view", parents=[CustomerPortal, EnterprisePortal])
    class SharedProfileChild:
        view = dummy_view

    EnterprisePortal.children = [SharedProfileChild]

    Route._create_tree(handed_classes=[CustomerPortal, EnterprisePortal])
    for key in General._tree_map:
        print(1111111111111, key)
    assert General._tree_map["/customer/profile-view"]._class == General._tree_map["/enterprise/profile-view"]._class
