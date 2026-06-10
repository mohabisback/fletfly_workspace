# fletfly/tests/classes/test_decorators.py
import pytest
from fletfly import Route, General, General, view, layout, fly_in, fly_out

def dummy_view(page): pass
def dummy_layout(page): pass

def test_01():
    # Scenario: Class has methods decorated with fletfly attributes.
    # The method name must be recorded in _clsattr fields, and extra attributes must diffuse.
    
    class DecoratedRoute:
        @view(hero=True)
        def my_custom_view(page): pass
        
        @layout(hero=True, override=False)
        def my_custom_layout(page): pass
        

    route, kids = Route._route_from_class(DecoratedRoute)
    
    assert route.view_clsattr["func"] == "my_custom_view"
    assert route.layout_clsattr["func"] == "my_custom_layout"
    # Ensure nested _fletfly_ attributes are stripped and diffused to the route object
    assert getattr(route, "_view_hero", None) is True
    assert getattr(route, "_layout_hero", None) is True
    assert getattr(route, "_layout_override", None) is False


def test_duplicate_decorators_throw_value_error():
    # Scenario: A class accidentally defines two separate functions for the same core mechanism
    # (e.g., two view functions). This must explicitly trigger a ValueError.
    
    class BrokenRoute:
        @view
        def view_one(page): pass
        @view(hero=True)      
        def view_two(page): pass

    with pytest.raises(ValueError) as exc_info:
        Route._route_from_class(BrokenRoute)
        
    assert "already has a view function named" in str(exc_info.value)


def test_accumulative_decorators_append_instead_of_overwriting():
    # Scenario: fly_ins and fly_outs can have multiple decorators/guards on different functions.
    # They should accumulate inside a list rather than overwriting each other.
    
    class GuardedRoute:
        @fly_in
        def check_auth(): pass
        @fly_in
        def check_premium(): pass

    route, kids = Route._route_from_class(GuardedRoute)
    
    assert isinstance(route.fly_ins, list)
    assert isinstance(route.fly_ins, list)
    assert len(route.fly_ins) == 2
    assert route.fly_ins[0]["func"]=="check_auth"
    assert route.fly_ins[1]["func"]=="check_premium"