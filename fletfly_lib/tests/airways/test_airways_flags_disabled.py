# fletfly/tests/routes/test_route_flags_disabled.py
import pytest
from fletfly import Router, Route, General

def dummy_view(page): pass

def test_detect_created_routes_disabled():
    # Scenario: When detect_created_routes is False, the pending routes queue 
    # must be completely ignored, processing ONLY the manually handed routes pool.
    General.detect_created_routes = False

    # Source 1: Handed manually
    manual_route = Route("manual-gate", view=dummy_view)

    # Source 2: Pending queue (Should be ignored)
    pending_route = Route("pending-gate", view=dummy_view)
    General._pending_routes.add(pending_route)

    Route._create_tree(routes=[manual_route])

    assert "/manual-gate" in General._main_zone_tree
    assert "/pending-gate" not in General._main_zone_tree



def dummy_view(page): pass

def test_auto_naming_with_disabled_detection():

    route = Route()
    @route
    class User:
        view = dummy_view

    # Trigger tree creation
    Route._create_tree(test_module=__name__)

    # Assert that the route was successfully registered with the lowercase name
    assert "/user" in General._main_zone_tree