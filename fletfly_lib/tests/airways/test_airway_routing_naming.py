# fletfly/tests/classes/test_routes_routing_naming.py
import pytest
from fletfly import Router, Route, General

def user_profile_page(page):
    pass

def test_automatic_path_naming_for_route_instances():
    # Scenario: If Router.auto_path_naming is True and the Route instance has no explicit path,
    # it must fall back to the normalized name of its view function during tree creation.
    Router.auto_path_naming = True
    Router.detect_created_routes = True
    
    route = Route(view=user_profile_page)
    
    Route._create_tree([route], test_module=__name__)
    
    assert route.path == "user-profile-page"


def test_auto_path_naming_with_layout_fallback():
    # Scenario: If view is not present, it should fall back to the layout function name.

    def control_center(page):
        pass
        
    route = Route(layout=control_center)
    
    Route._create_tree([route], test_module=__name__)
    
    assert route.path == "control-center"


def test_fallback_naming_disabled_configuration():
    # Scenario: If Router.auto_path_naming is False, the path must remain None
    # even if a view function is provided.
    Router.auto_path_naming = False
    Router.detect_created_routes = True
    
    route = Route(_view=user_profile_page)
    General._pending_routes = {route}
    
    with pytest.raises(ValueError):
        Route._create_tree(test_module=__name__)
    assert route._path is None