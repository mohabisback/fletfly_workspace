# fletfly/tests/test_chaining.py
from fletfly import Route, General

def test_route_full_chaining():
    def f1(): return "f1"
    def f2(): return "f2"
    def f3(): return "f3"
    def f4(): return "f4"
    
    aw = Route(fly_ins=[f1, (f2, {"role":"user", "apply_per_view":True})])
    # Chain everything
    aw.path('home')\
      .fly_to('target')\
      .layout_override(True)\
      .fly_in_override(False)\
      .fly_out_override(None)\
      .title('My Title')\
      .icon('my-icon')\
      .props({'a': 1})\
      .fly_in(f3, role="user", apply_per_view=True)\
      .middleware(f4)\
      .fly_outs([f1, (f2, {"role":"user", "apply_per_view":True})])\
      .fly_out(f3)\
      .children([
        Route('sub1').fly_to("home"),
        Route('sub2').icon("my_icon"),
        Route('sub3').title("my_title")
                ])
    aw.child("sub4").fly_to("home")
    aw4 = aw.child("sub4").redirect("home")
    aw4.frame = f1
    #aw.is_zone = None
    aw.view_hero = True
    aw.layout_hero = False

    # Assertions
    assert aw.props == {'a': 1}
    assert aw.path == 'home'
    assert aw.fly_to == 'target'
    assert aw.layout_override == True
    assert aw.layout_override is not True
    assert aw._layout_override is True
    assert aw.fly_in_override == False
    assert aw.fly_in_override is not False
    assert aw._fly_in_override is False
    assert aw.fly_out_override == None
    assert aw.fly_out_override is not None
    assert aw._fly_out_override is None
    assert aw.view_hero == True
    assert aw.layout_hero == False
    assert aw.title == 'My Title'
    assert aw.icon == 'my-icon'
    assert len(aw.fly_ins) == 4
    assert aw.fly_ins[0]["func"] == f1
    assert aw.fly_ins[0]["inheritable"] is True
    assert aw.fly_ins[0]["apply_per_view"] is False
    assert aw.fly_ins[1]["func"] == f2
    assert aw.fly_ins[1]["props"]["role"] == "user"
    assert aw.fly_ins[1]["inheritable"] is True
    assert aw.fly_ins[1]["apply_per_view"] is True
    assert aw.fly_outs[0]["func"] == f1
    assert aw.fly_outs[1]["func"] == f2
    assert len(aw.fly_outs) == 3
    assert len(aw.children) == 5
    assert aw.children[0].path == "sub1"
    assert aw.children[1].path == "sub2"
    assert aw.children[2].path == "sub3"
    assert aw.children[3].path == "sub4"
    assert aw.children[4].fly_to == "home"
    assert aw.children[4]._layout["func"] == f1