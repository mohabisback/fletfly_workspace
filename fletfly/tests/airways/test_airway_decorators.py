# fletfly/tests/airways/test_airway_decorators.py
import pytest
from fletfly import Airway

def test_01_pure_airway_decorators_diffusion():
    # Scenario: Standalone functions decorated with Airway object methods (@route.build, @route.layout).
    # The function references must be recorded in pure airway fields (_build, _layout), 
    # and extra attributes must diffuse directly to the airway instance.
    
    route = Airway("decorated-route")
    
    def my_custom_build(page): pass
    
    def my_custom_layout(page): pass
    
    route.build(my_custom_build, hero=True)
    route.layout(my_custom_layout, hero=True, override=False)

    # Verify that the pure airway instance caught the function references
    assert route._build["func"] == my_custom_build
    assert route._layout["func"] == my_custom_layout
    
    # Ensure nested metadata attributes are stripped and diffused directly to the airway object
    assert getattr(route, "_build_hero", None) is True
    assert getattr(route, "_layout_hero", None) is True
    assert getattr(route, "_layout_override", None) is False


def test_accumulative_airway_decorators_append_instead_of_overwriting():
    # Scenario: fly_ins and fly_outs can have multiple decorators/guards on different functions.
    # For pure Airway objects, they should accumulate inside the fly_ins list rather than overwriting.
    
    route = Airway("guarded-route")

    def check_auth(): pass
    
    def check_premium(): pass
    route.fly_in(check_auth)
    route.fly_in(check_premium)

    # Verify that both functions are captured sequentially inside the list
    assert isinstance(route.fly_ins, list)
    assert len(route.fly_ins) == 2
    assert route.fly_ins[0]["func"] == check_auth
    assert route.fly_ins[1]["func"] == check_premium
