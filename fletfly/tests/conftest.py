# fletfly/tests/conftest.py
import pytest
from fletfly import Airway, Airline

@pytest.fixture(autouse=True)
def reset_fletfly_state():
    """
    Automatically reset the global state of Airway and Airline before each test 
    to prevent test pollution caused by Singletons and class-level maps.
    """
    Airway._map.clear()
    Airway._pending_airways.clear()
    Airway._registered_children.clear()
    Airway._map.clear()
    Airline._instance = None
    Airline.auto_path_naming = True
    Airline.detect_path_routes = True
    Airline.detect_airway_subclasses = True
    Airline.detect_inner_classes = True
    Airline.detect_method_routes = True
    yield