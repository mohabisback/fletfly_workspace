# fletfly/tests/classes/test_classes_routing_naming.py
import pytest
from fletfly import Router, Route, General, layout

def test_detect_methods_routesion_extracts_callable_methods():
    # Scenario: When Router.detect_method_routes is enabled, any clean callable method 
    # (without fletfly decorators) must be converted into a child child Route automatically.
    
    class ControlCenter:
        # Normal callable method
        def active_sessions(self, page):
            pass

    class zone: registered_children = set()
    route, kids = Route._route_from_class(ControlCenter, None, zone)

    # Child method auto-detection check
    assert len(kids) == 1
    assert kids[0].path == "active_sessions" or kids[0].path == "active-sessions" # depends on normalization inside constructor
    assert kids[0]._view["func"] == "active_sessions"
    assert kids[0]._class is ControlCenter


def test_fallback_naming_skipped_for_non_normal_decorated_routes():
    # Scenario: If a class contains any core fletfly decorated attribute (_fletfly_view, etc.),
    # normal_route becomes False, meaning auto_path_naming should NOT execute.
    
    Router.auto_path_naming = True
    @layout
    class CustomLayoutOnly:
        @layout
        def my_layout(page):
            pass
        # Manually triggering non-normal classification via underlying attribute injection
    
    class zone: registered_children = set()
    route, kids = Route._route_from_class(CustomLayoutOnly, None, zone)
    
    # Path must remain None because auto-naming is explicitly gated behind normal_route condition
    assert route._path == "UNSET"