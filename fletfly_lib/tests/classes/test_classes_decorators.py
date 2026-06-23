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
        
    class zone: registered_children = set()
    route, kids = Route._route_from_class(DecoratedRoute, None, zone)
    
    assert route._view["func"] == "my_custom_view"
    assert route._layout["func"] == "my_custom_layout"
    
    for item in route.__dict__:
        print(item)
    
    # Ensure nested _fletfly_ attributes are stripped and diffused to the route object
    assert route._view_hero == True
    assert route._layout_hero == True
    assert route._layout_override == False


def test_accumulative_decorators_append_instead_of_overwriting():
    # Scenario: fly_ins and fly_outs can have multiple decorators/guards on different functions.
    # They should accumulate inside a list rather than overwriting each other.
    
    class GuardedRoute:
        @fly_in
        def check_auth(): pass
        @fly_in
        def check_premium(): pass

    class zone: registered_children = set()
    route, kids = Route._route_from_class(GuardedRoute, None, zone)

    assert isinstance(route.fly_ins, list)
    assert len(route.fly_ins) == 2
    assert route.fly_ins[0]["func"]=="check_auth"
    assert route.fly_ins[1]["func"]=="check_premium"