# fletfly/tests/routes/test_route_decorators.py
import pytest
from fletfly import Route, General

def test_01_pure_route_decorators_diffusion():
    # Scenario: Standalone functions decorated with Route object methods (@route.view, @route.layout).
    # The function references must be recorded in pure route fields (_view, _layout), 
    # and extra attributes must diffuse directly to the route instance.
    
    route = Route("decorated-route")
    
    def my_custom_view(page): pass
    
    def my_custom_layout(page): pass
    
    route.view(my_custom_view, hero=True)
    route.layout(my_custom_layout, hero=True, override=False)

    # Verify that the pure route instance caught the function references
    assert route._view["func"] == my_custom_view
    assert route._layout["func"] == my_custom_layout
    
    # Ensure nested metadata attributes are stripped and diffused directly to the route object
    assert route._view_hero == True
    assert route._layout_hero == True
    assert route._layout_override == False


def test_accumulative_route_decorators_append_instead_of_overwriting():
    # Scenario: fly_ins and fly_outs can have multiple decorators/guards on different functions.
    # For pure Route objects, they should accumulate inside the fly_ins list rather than overwriting.
    
    route = Route("guarded-route")

    def check_auth(): pass
    
    def check_premium(): pass
    route.fly_in(check_auth)
    route.fly_in(check_premium)

    # Verify that both functions are captured sequentially inside the list
    assert isinstance(route.fly_ins, list)
    assert len(route.fly_ins) == 2
    assert route.fly_ins[0]["func"] == check_auth
    assert route.fly_ins[1]["func"] == check_premium
