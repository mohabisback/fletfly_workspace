# fletfly/tests/classes/test_routing_naming.py
import pytest
from fletfly import Airway, Airline, layout

def test_automatic_path_naming_for_normal_airways():
    # Scenario: If Airline.auto_path_naming is True and the class has no explicit path attribute,
    # it must fall back to the lowercase class name with underscores replaced by hyphens.
    
    Airline.auto_path_naming = True
    
    class User_Profile_Page:
        # A normal clean class with no decorators or explicit path
        pass

    airway, kids = Airway._airway_from_class(User_Profile_Page)
    
    # Verify that the path was automatically derived and normalized
    assert airway.path == "user-profile-page"


def test_detect_methods_routesion_extracts_callable_methods():
    # Scenario: When Airline.detect_method_routes is enabled, any clean callable method 
    # (without fletfly decorators) must be converted into a subway child Airway automatically.
    
    Airline.detect_method_routes = True
    Airline.auto_path_naming = True
    
    class ControlCenter:
        # Normal callable method
        def active_sessions(self, page):
            pass

    airway, kids = Airway._airway_from_class(ControlCenter)
    
    # Parent class fallback name check
    assert airway.path == "control-center"
    
    # Child method auto-detection check
    assert len(kids) == 1
    assert kids[0].path == "active_sessions" or kids[0].path == "active-sessions" # depends on normalization inside constructor
    assert kids[0].build_clsattr == "active_sessions"
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
    assert airway.path is None