# fletfly/tests/classes/test_classes_dict.py
import pytest
import fletfly
from fletfly import (
    Router,
    Route, 
    UseFunc, 
    UseFunc
)

def test_route_from_class_undecorated_method_dict():
    """Test that an undecorated view method wrapped via aliases stores a UseFunc."""
    # Ensure route detection configuration is enabled
        
    class MockCBV:
        # Standard instance method representing the view function
        def view(self, page):
            pass
    
    class zone: registered_children = set()
    
    class zone: registered_children = set()
    route, kids = Route._route_from_class(MockCBV, None, zone)
    # Verify that view_clsattr holds the dict representation instead of a plain string
    assert hasattr(route, "view")
    assert isinstance(route._view, UseFunc)
    assert route.view["func"] == "view"


def test_route_from_class_static_decorated_method():
    """Test that methods explicitly flagged with _fletfly_static assign function objects directly."""
    class MockStaticCBV:
        def layout(self, page):
            pass
    
    # Simulating the presence of the static marker on the function
    getattr(MockStaticCBV.layout, "__dict__")["_fletfly_static"] = True


    class zone: registered_children = set()
    route, kids = Route._route_from_class(MockStaticCBV, None, zone)
    
    # According to the second loop logic, static flagged sets the official_name attribute directly
    assert hasattr(route, "_layout")
    assert isinstance(route._layout, UseFunc)
    assert route._layout["func"] == "layout"


def test_route_from_class_automated_method_routing_kids():
    """Test that automated method routing fallback correctly creates kid routes with dict viewers."""
    Router.detect_method_routes = True
    
    class AutomatedRoutesCBV:
        def dashboard_view(self, page):
            pass

    # Forcing a clean route scenario without main flags

    class zone: registered_children = set()
    route, func_kids = Route._route_from_class(AutomatedRoutesCBV, None, zone)
    
    # Find the child route generated for dashboard_view
    assert len(func_kids) == 1
    assert isinstance(func_kids[0], Route)
    assert func_kids[0]._view["func"] == "dashboard_view"


def test_route_from_class_undecorated_fly_in_out_accumulation():
    """Test that undecorated fly_in methods append a UseFunc to the clsattr tracker."""
    class MockMiddlewareCBV:
        def fly_in(self, page):
            pass
            
    class zone: registered_children = set()
    route, class_kids = Route._route_from_class(MockMiddlewareCBV, None, zone)
    
    # Verify that fly_ins correctly accumulates the UseFunc wrapper
    assert hasattr(route, "fly_ins")
    assert isinstance(route.fly_ins, list)
    assert len(route.fly_ins) == 1
    assert isinstance(route.fly_ins[0], UseFunc)
    assert route.fly_ins[0]["func"] == "fly_in"