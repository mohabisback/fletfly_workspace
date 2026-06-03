# fletfly/tests/classes/test_classes_flags_disabled.py
import pytest
from fletfly import Airway, Airline, layout

def dummy_build(page): pass

def test_auto_path_naming_disabled():
    # Scenario: When auto_path_naming is False, a normal class without an explicit path 
    # attribute must NOT have its path auto-derived. It should remain None.
    
    Airline.auto_path_naming = False

    class SilentRoute:
        build = dummy_build

    airway, kids = Airway._airway_from_class(SilentRoute)
    
    # Path must strictly remain None because auto-naming is turned off
    assert airway.path is None


def test_detect_methods_routes_disabled():
    # Scenario: When detect_method_routes is False, clean callable methods inside a class 
    # must be completely ignored and NOT extracted as implicit subways/child airways.
    
    Airline.detect_method_routes = False

    class DashboardPage:
        # This clean callable should be skipped entirely
        def settings(self, page): pass

    airway, kids = Airway._airway_from_class(DashboardPage)
    
    # Parent path can be auto-named, but kids list must be completely empty
    assert airway.path == "dashboard-page"
    assert len(kids) == 0

def test_inheritance_and_decorations_disabled_inside_append_classes():
    # Scenario: When detect_airway_subclasses and detect_decorated_classes are both False, 
    # _append_classes must completely ignore pending decorated queues and subclass trees,
    # processing ONLY the manually handed classes pool.
    
    Airline.detect_decorated_classes = False
    Airline.detect_airway_subclasses = False
    Airline.auto_path_naming = True

    Airway._map.clear()
    Airway._registered_children.clear()

    # Source 1: Handed manually (Should be processed)
    class ManuallyHandedRoute:
        path = "manual-gate"
        _build = dummy_build

    # Source 2: Pending queue (Should be completely ignored)
    class DecorativeRoute:
        path = "deco-gate"
        _build = dummy_build
    Airway._pending_classes = {DecorativeRoute}

    # Source 3: Inherited from Airway (Should be completely ignored)
    class SubclassRoute(Airway):
        path = "subclass-gate"
        _build = dummy_build

    # Execute consolidation with only manual routes passed
    Airway._create_tree(handed_classes=[ManuallyHandedRoute])

    # Assertions
    # 1. Manual source must be processed and injected successfully
    assert "/manual-gate" in Airway._map

    # 2. Both disabled discovery source vectors must NOT bleed into the tree map
    assert "/deco-gate" not in Airway._map
    assert "/subclass-gate" not in Airway._map

    # Clean global states
    Airway._pending_classes.clear()