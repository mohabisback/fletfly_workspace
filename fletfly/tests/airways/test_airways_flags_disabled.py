# fletfly/tests/airways/test_airway_flags_disabled.py
import pytest
from fletfly import Airway, Airline

def dummy_build(page): pass

def test_detect_path_routes_disabled():
    # Scenario: When detect_path_routes is False, the pending airways queue 
    # must be completely ignored, processing ONLY the manually handed airways pool.
    Airline.detect_path_routes = False

    # Source 1: Handed manually
    manual_airway = Airway("manual-gate", build=dummy_build)

    # Source 2: Pending queue (Should be ignored)
    pending_airway = Airway("pending-gate", build=dummy_build)
    Airway._pending_airways.add(pending_airway)

    Airway._create_tree(handed_classes=[manual_airway])

    assert "/manual-gate" in Airway._map
    assert "/pending-gate" not in Airway._map

    Airway._pending_airways.clear()


    # fletfly/tests/classes/test_classes_flags_disabled.py
import pytest
from fletfly import Airway, Airline

def dummy_build(page): pass

def test_auto_naming_with_disabled_detection():
    Airline.auto_path_naming = True

    route = Airway()
    @route
    class User:
        build = dummy_build

    # Trigger tree creation
    Airway._create_tree(handed_classes=None)

    # Assert that the route was successfully registered with the lowercase name
    assert "/user" in Airway._map