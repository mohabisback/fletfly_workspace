# test_decorators.py
import pytest
from fletfly import Airway, build, layout, fly_in, fly_out

def dummy_build(page): pass
def dummy_layout(page): pass

def test_01():
    # Scenario: Class has methods decorated with fletfly attributes.
    # The method name must be recorded in _clsattr fields, and extra attributes must diffuse.
    
    class DecoratedRoute:
        @build(hero=True)
        def my_custom_build(page): pass
        
        @layout(hero=True, override=False)
        def my_custom_layout(page): pass
        

    airway, kids = Airway._airway_from_class(DecoratedRoute)
    
    assert airway.build_clsattr == "my_custom_build"
    assert airway.layout_clsattr == "my_custom_layout"
    # Ensure nested _fletfly_ attributes are stripped and diffused to the airway object
    assert getattr(airway, "build_hero", None) is True
    assert getattr(airway, "layout_hero", None) is True
    assert getattr(airway, "layout_override", None) is False


def test_duplicate_decorators_throw_value_error():
    # Scenario: A class accidentally defines two separate functions for the same core mechanism
    # (e.g., two build functions). This must explicitly trigger a ValueError.
    
    class BrokenRoute:
        @build
        def build_one(page): pass
        @build(hero=True)      
        def build_two(page): pass

    with pytest.raises(ValueError) as exc_info:
        Airway._airway_from_class(BrokenRoute)
        
    assert "already has a build function named" in str(exc_info.value)


def test_accumulative_decorators_append_instead_of_overwriting():
    # Scenario: fly_ins and fly_outs can have multiple decorators/guards on different functions.
    # They should accumulate inside a list rather than overwriting each other.
    
    class GuardedRoute:
        @fly_in
        def check_auth(): pass
        @fly_in
        def check_premium(): pass

    airway, kids = Airway._airway_from_class(GuardedRoute)
    
    assert isinstance(airway.fly_ins, list)
    assert isinstance(airway.fly_ins_clsattr, list)
    assert len(airway.fly_ins_clsattr) == 2
    assert "check_auth" in airway.fly_ins_clsattr
    assert "check_premium" in airway.fly_ins_clsattr