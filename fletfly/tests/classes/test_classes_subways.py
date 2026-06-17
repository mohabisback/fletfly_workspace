# fletfly/tests/classes/test_classes_child_decorator.py
import pytest
from fletfly import Route, General, Router, child

def dummy_view(page):
    pass

def test_child_explicit_path_and_diffusion():
    # Scenario 1: Method decorated with @child(path="...") explicit literal string.
    # The explicit path must be captured directly without triggering delayed runtime lookups,
    # and any extra metadata attributes must diffuse into the child route object correctly.
    class zone: registered_children=set()
    class Dashboard:
        path = "main-dash"
        
        @child(path="user-analytics")
        def analytics(cls, page):
            pass

    route, kids = Route._route_from_class(Dashboard, None, zone=zone)
    
    assert len(kids) == 1
    sub_route = kids[0]
    
    # Assert explicit path is locked directly from decorator arguments
    assert sub_route.path == "user-analytics"
    
    # Assert the actual function identifier is tracked for rendering execution
    assert sub_route.view["func"] == "analytics"
    
    # Assert attribute diffusion mechanics worked with appropriate namespacing

def test_child_integration_in_global_map():
    # Scenario 3: Complete integration testing via the consolidation pipeline.
    # A class with a @child decorated method must cleanly inject its child route 
    # under the parent route tree without any data isolation issues.

    @Route
    class CorporatePortal:
        path = "portal"
        view = dummy_view
        
        @child(path="financial-reports")
        def reports(self, page):
            pass

    # Execute consolidation pool processing
    Route._create_tree(__name__)

    # Assertions for complete hierarchical registration inside the routing engine map
    assert "/portal" in General._main_zone_tree
    assert "/portal/financial-reports" in General._main_zone_tree
    
    # Verify the child execution context points back to the parent component
    assert General._main_zone_tree["/portal/financial-reports"]._class is CorporatePortal
    assert General._main_zone_tree["/portal/financial-reports"]._view["func"] == "reports"
    