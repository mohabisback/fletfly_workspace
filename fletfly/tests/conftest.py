import pytest
from fletfly import Airway, Airline

@pytest.fixture(autouse=True)
def reset_fletfly_state():
    """
    Automatically reset the global state of Airway and Airline before each test 
    to prevent test pollution caused by Singletons and class-level maps.
    """
    Airway._map.clear()
    Airway._airways_all.clear()
    Airway._airways_wild.clear()
    Airway._registered_children_classes.clear()
    Airway._pending_classes.clear()
    Airline._instance = None
    yield