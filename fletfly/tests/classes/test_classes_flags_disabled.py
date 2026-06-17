# fletfly/tests/classes/test_classes_flags_disabled.py
import pytest
from fletfly import Route, General, Router, layout

def dummy_view(page): pass

def test_auto_path_naming_disabled():
    # Scenario: When auto_path_naming is False, a normal class without an explicit path 
    # attribute must NOT have its path auto-derived. It should remain None.
    
    Router.auto_path_naming = False

    class SilentRoute:
        view = dummy_view

    class zone: registered_children = set()
    route, kids = Route._route_from_class(SilentRoute, None, zone)
    
    # Path must strictly remain None because auto-naming is turned off
    assert route._path is None


def test_detect_methods_routes_disabled():
    # Scenario: When detect_method_routes is False, clean callable methods inside a class 
    # must be completely ignored and NOT extracted as implicit children/child routes.
    
    General.detect_method_routes = False

    class DashboardPage:
        # This clean callable should be skipped entirely
        def settings(self, page): pass

    class zone: registered_children = set()
    route, kids = Route._route_from_class(DashboardPage, None, zone)
    
    # Parent path can be auto-named, but kids list must be completely empty
    assert route._class == DashboardPage
    assert len(kids) == 0

def test_inheritance_and_decorations_disabled_inside_append_classes():
    # _append_classes must completely ignore pending decorated queues and subclass trees,
    # processing ONLY the manually handed classes pool.
    
    General.detect_route_subclasses = False
    General.auto_path_naming = True

    # Source 1: Handed manually (Should be processed)
    class ManuallyHandedRoute:
        path = "manual-gate"
        _view = dummy_view

    # Source 2: Pending queue (Should be completely ignored)
    class DecorativeRoute:
        path = "deco-gate"
        _view = dummy_view
    General._pending_classes = {DecorativeRoute}

    # Source 3: Inherited from Route (Should be completely ignored)
    class SubclassRoute(Route):
        path = "subclass-gate"
        _view = dummy_view

    # Execute consolidation with only manual routes passed
    Route._create_tree(anchors=[ManuallyHandedRoute])

    # Assertions
    # 1. Manual source must be processed and injected successfully
    assert "/manual-gate" in General._main_zone_tree

    # 2. Both disabled discovery source vectors must NOT bleed into the tree map
    assert "/deco-gate" not in General._main_zone_tree
    assert "/subclass-gate" not in General._main_zone_tree
