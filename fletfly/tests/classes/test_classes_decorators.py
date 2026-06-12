# fletfly/tests/classes/test_decorators.py

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
    
    assert route._view["func"] == "my_custom_view"
    assert route._layout["func"] == "my_custom_layout"
    
    for item in route.__dict__:
        print(item)
    
    # Ensure nested _fletfly_ attributes are stripped and diffused to the route object
    assert getattr(route, "_view_hero", None) is True
    assert getattr(route, "_layout_hero", None) is True
    assert getattr(route, "_layout_override", None) is False


def test_duplicate_decorators_throw_value_error(capsys):
    # Scenario: A class accidentally defines two separate functions for the same core mechanism
    # (e.g., two view functions). This must explicitly trigger a ValueError.
    
    class BrokenRoute:
        @view
        def view_one(page): pass
        @view(hero=True)      
        def view_two(page): pass

    Route._route_from_class(BrokenRoute)
    
    captured = capsys.readouterr()
    
    assert "[fletfly] WARNING: second re-setting of view"  in captured.out
    

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