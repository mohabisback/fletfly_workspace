# fletfly/tests/conftest.py
import pytest
from fletfly import General

@pytest.fixture(autouse=True)
def reset_fletfly_state():
    """
    Automatically reset the global state of before each test 
    to prevent test pollution caused by Singletons and class-level maps.
    """
    General._tree_map.clear()
    General._pending_routes.clear()
    General._registered_children.clear()
    General._tree_map.clear()
    General._router_instance= None
    General.auto_path_naming = True
    General.detect_path_routes = True
    General.detect_route_subclasses = True
    General.detect_inner_classes = True
    General.detect_method_routes = True
    yield