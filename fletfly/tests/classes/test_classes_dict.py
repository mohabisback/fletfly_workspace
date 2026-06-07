# fletfly/tests/classes/test_classes_dict.py
import pytest
import fletfly
from fletfly import (
    Airway, 
    Airline, 
    _BuildLayoutDict, 
    _FlyInOutDict
)

def test_airway_from_class_undecorated_method_dict():
    """Test that an undecorated view method wrapped via aliases stores a _BuildLayoutDict."""
    # Ensure route detection configuration is enabled
        
    class MockCBV:
        # Standard instance method representing the build function
        def build(self, page):
            pass
        
    airway, class_kids = Airway._airway_from_class(MockCBV)
    
    # Verify that build_clsattr holds the dict representation instead of a plain string
    assert hasattr(airway, "build_clsattr")
    assert isinstance(airway.build_clsattr, _BuildLayoutDict)
    assert airway.build_clsattr["func"] == "build"


def test_airway_from_class_static_decorated_method():
    """Test that methods explicitly flagged with _fletfly_static assign function objects directly."""
    class MockStaticCBV:
        def layout(self, page):
            pass
    
    # Simulating the presence of the static marker on the function
    getattr(MockStaticCBV.layout, "__dict__")["_fletfly_static"] = True

    airway, class_kids = Airway._airway_from_class(MockStaticCBV)
    
    # According to the second loop logic, static flagged sets the official_name attribute directly
    assert hasattr(airway, "layout")
    assert isinstance(airway.layout_clsattr, _BuildLayoutDict)
    assert airway.layout_clsattr["func"] == "layout"


def test_airway_from_class_automated_method_routing_kids():
    """Test that automated method routing fallback correctly creates kid airways with dict builders."""
    Airline.detect_method_routes = True
    
    class AutomatedRoutesCBV:
        def dashboard_view(self, page):
            pass

    # Forcing a clean airway scenario without main flags
    airway, func_kids = Airway._airway_from_class(AutomatedRoutesCBV)
    
    # Find the child airway generated for dashboard_view
    target_kid = next((kid for kid in func_kids if kid.path == "dashboard-view"), None)
    assert target_kid is not None
    assert isinstance(target_kid.build_clsattr, _BuildLayoutDict)
    assert target_kid.build_clsattr["func"] == "dashboard_view"


def test_airway_from_class_undecorated_fly_in_out_accumulation():
    """Test that undecorated fly_in methods append a _FlyInOutDict to the clsattr tracker."""
    class MockMiddlewareCBV:
        def fly_in(self, page):
            pass

    airway, class_kids = Airway._airway_from_class(MockMiddlewareCBV)
    
    # Verify that fly_ins correctly accumulates the _FlyInOutDict wrapper
    assert hasattr(airway, "fly_ins")
    assert isinstance(airway.fly_ins, list)
    assert len(airway.fly_ins) == 1
    assert isinstance(airway.fly_ins[0], _FlyInOutDict)
    assert airway.fly_ins[0]["func"] == "fly_in"