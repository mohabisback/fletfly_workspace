# fletfly/tests/airways/test_airway_decorators.py
import pytest
from fletfly import Airway

def test_01_pure_airway_decorators_diffusion():
    # Scenario: Standalone functions decorated with Airway object methods (@route.build, @route.layout).
    # The function references must be recorded in pure airway fields (_build, _layout), 
    # and extra attributes must diffuse directly to the airway instance.
    
    route = Airway("decorated-route")
    
    @route.build(hero=True)
    def my_custom_build(page): pass
    
    @route.layout(hero=True, override=False)
    def my_custom_layout(page): pass
    

    # Verify that the pure airway instance caught the function references
    assert route._build == my_custom_build
    assert route._layout == my_custom_layout
    
    # Ensure nested metadata attributes are stripped and diffused directly to the airway object
    assert getattr(route, "build_hero", None) is True
    assert getattr(route, "layout_hero", None) is True
    assert getattr(route, "layout_override", None) is False


def test_duplicate_airway_decorators_throw_value_error():
    # Scenario: An Airway object accidentally decorates two separate standalone functions 
    # for the same core mechanism (e.g., two build functions). This must explicitly trigger a ValueError.
    
    route = Airway("broken-route")

    @route.build
    def build_one(page): pass

    # Decorating a second function on the same instance must raise a conflict error
    with pytest.raises(ValueError) as exc_info:
        @route.build(hero=True)      
        def build_two(page): pass
        
    assert "already has a build function" in str(exc_info.value)


def test_accumulative_airway_decorators_append_instead_of_overwriting():
    # Scenario: fly_ins and fly_outs can have multiple decorators/guards on different functions.
    # For pure Airway objects, they should accumulate inside the fly_ins list rather than overwriting.
    
    route = Airway("guarded-route")

    @route.fly_in
    def check_auth(): pass
    
    @route.fly_in
    def check_premium(): pass

    # Verify that both functions are captured sequentially inside the list
    assert isinstance(route.fly_ins, list)
    assert len(route.fly_ins) == 2
    assert check_auth in route.fly_ins
    assert check_premium in route.fly_ins