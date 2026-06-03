# fletfly/tests/classes/test_airways_routing_naming.py
import pytest
from fletfly import Airway, Airline

def user_profile_page(page):
    pass

def test_automatic_path_naming_for_airway_instances():
    # Scenario: If Airline.auto_path_naming is True and the Airway instance has no explicit path,
    # it must fall back to the normalized name of its build function during tree creation.
    Airline.auto_path_naming = True
    Airline.auto_detect_routes = True
    
    airway = Airway(_build=user_profile_page)
    Airway._pending_airways = {airway}
    
    Airway._create_tree()
    
    assert airway.path == "user-profile-page"


def test_auto_path_naming_with_layout_fallback():
    # Scenario: If build is not present, it should fall back to the layout function name.
    Airline.auto_path_naming = True
    Airline.auto_detect_routes = True
    
    def control_center(page):
        pass
        
    airway = Airway(_layout=control_center)
    Airway._pending_airways = {airway}
    
    Airway._create_tree()
    
    assert airway.path == "control-center"


def test_fallback_naming_disabled_configuration():
    # Scenario: If Airline.auto_path_naming is False, the path must remain None
    # even if a build function is provided.
    Airline.auto_path_naming = False
    Airline.auto_detect_routes = True
    
    airway = Airway(_build=user_profile_page)
    Airway._pending_airways = {airway}
    
    with pytest.raises(ValueError):
        Airway._create_tree()
    assert airway.path is None