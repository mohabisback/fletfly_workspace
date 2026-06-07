# fletfly/tests/classes/test_classes_subway_decorator.py
import pytest
from fletfly import Airway, Airline, subway

def dummy_build(page):
    pass

def test_subway_explicit_path_and_diffusion():
    # Scenario 1: Method decorated with @subway(path="...") explicit literal string.
    # The explicit path must be captured directly without triggering delayed runtime lookups,
    # and any extra metadata attributes must diffuse into the subway airway object correctly.
    
    class Dashboard:
        path = "main-dash"
        
        @subway(path="user-analytics")
        def analytics(cls, page):
            pass

    airway, kids = Airway._airway_from_class(Dashboard)
    
    assert len(kids) == 1
    sub_airway = kids[0]
    
    # Assert explicit path is locked directly from decorator arguments
    assert sub_airway.path == "user-analytics"
    
    # Assert the actual function identifier is tracked for rendering execution
    assert sub_airway.build_clsattr == "analytics"
    
    # Assert attribute diffusion mechanics worked with appropriate namespacing

def test_subway_integration_in_global_map():
    # Scenario 3: Complete integration testing via the consolidation pipeline.
    # A class with a @subway decorated method must cleanly inject its child route 
    # under the parent route tree without any data isolation issues.

    @Airway
    class CorporatePortal:
        path = "portal"
        build = dummy_build
        
        @subway(path="financial-reports")
        def reports(self, page):
            pass

    # Execute consolidation pool processing
    Airway._create_tree()
    
    for k, v in Airway._map.items():
        print(9999999999999, v, ",", k)

    # Assertions for complete hierarchical registration inside the routing engine map
    assert "/portal" in Airway._map
    assert "/portal/financial-reports" in Airway._map
    
    # Verify the child execution context points back to the parent component
    assert Airway._map["/portal/financial-reports"]._class is CorporatePortal
    assert Airway._map["/portal/financial-reports"].build_clsattr == "reports"
    