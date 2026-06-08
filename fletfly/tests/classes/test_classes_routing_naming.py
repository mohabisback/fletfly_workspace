# fletfly/tests/classes/test_classes_routing_naming.py
import pytest
from fletfly import Airway, Airline, layout

def test_detect_methods_routesion_extracts_callable_methods():
    # Scenario: When Airline.detect_method_routes is enabled, any clean callable method 
    # (without fletfly decorators) must be converted into a subway child Airway automatically.
    
    class ControlCenter:
        # Normal callable method
        def active_sessions(self, page):
            pass

    airway, kids = Airway._airway_from_class(ControlCenter)
    

    # Child method auto-detection check
    assert len(kids) == 1
    assert kids[0].path == "active_sessions" or kids[0].path == "active-sessions" # depends on normalization inside constructor
    assert kids[0].build_clsattr["func"] == "active_sessions"
    assert kids[0]._class is ControlCenter


def test_fallback_naming_skipped_for_non_normal_decorated_airways():
    # Scenario: If a class contains any core fletfly decorated attribute (_fletfly_build, etc.),
    # normal_airway becomes False, meaning auto_path_naming should NOT execute.
    
    Airline.auto_path_naming = True
    @layout
    class CustomLayoutOnly:
        @layout
        def my_layout(page):
            pass
        # Manually triggering non-normal classification via underlying attribute injection
    
    airway, kids = Airway._airway_from_class(CustomLayoutOnly)
    
    # Path must remain None because auto-naming is explicitly gated behind normal_airway condition
    assert airway._path is None