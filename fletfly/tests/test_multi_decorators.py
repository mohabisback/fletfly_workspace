# fletfly/tests/test_multi_decorators.py
import pytest
from fletfly import fly_in, fly_out, layout, build, subway, Airway
import fletfly

def test_subway_class_inject():
    @Airway("")
    @Airway("home")
    class Parent(Airway):
        @subway
        @Airway.subway(path='third', hero=True, width=100, props={"height": 200}) # override not expected
        @subway(path='second', fly_to="/", width=100, props={"height": 200})
        @Airway.subway(path='first', width=100, props={"height": 200})
        class MyClass():
            pass
        

        #res0 = subway(MyClass) # same as @subway/my_func (must be recorded)
        #assert res0 == MyClass
        #res1 = Airway.subway(MyClass) # same as @Airway.subway/my_func (must be recorded)
        #assert res1 == MyClass 
        
        res2 = Airway("about", role = "admin")
        res3 = res2.subway("page1", role = "user")
        assert res2.path == "about"
        assert res2.props.get("role", "not there") == "admin"
        assert res2.subways[0] == res3
        assert res3.path == "page1"
        assert res3.props.get("role", "not there") == "user"
        
        res4 = res2.subway(MyClass, "page2", role="user")
        assert res4.path == "page2"
        assert res4._class == MyClass
        assert res4.props["role"] == "user"
            
        res5 = Airway.subway("page3", MyClass, [res2, res3], role="user")
        assert res5.path == "page3"
        assert res5._class == MyClass
        assert res5.props["role"] == "user"
            

        res6 = getattr(MyClass, "_fletfly_subway", [])
        
        assert len(res6) == 4
        assert res6[0].get("path", "not there") == "first"
        assert res6[0].get("fly_to", "not there") == "not there"
        assert res6[0].get("props",{}).get("width") == 100
        assert res6[0].get("props",{}).get("height") == 200
        
        assert res6[1].get("path", "not there") == "second"
        assert res6[1].get("fly_to", "not there") == "/"
        assert res6[1].get("props",{}).get("width") == 100
        assert res6[1].get("props",{}).get("height") == 200
        
        assert res6[2].get("path", "not there") == "third"
        assert res6[2].get("fly_to", "not there") == "not there"
        assert res6[2].get("props",{}).get("width") == 100
        assert res6[2].get("props",{}).get("height") == 200
        
        assert res6[3].get("path", "not there") == "not there"
        assert res6[3].get("fly_to", "not there") == "not there"
        assert res6[3].get("props", "not there") == {}

    


def test_inject_method():
    @fly_out
    @fly_out(override=False, apply_per_view=False, width=100, props={"height":200}) # inheritable has a default = True    
    @fly_in(override=False, apply_per_view=True, width=100, props={"height":200}) # inheritable has a default = True
    @fly_in(override=False, apply_per_view=False, width=100, props={"height":200}) # inheritable has a default = True
    @build(override=False, width=100, props={"height": 200}) # override not expected
    @Airway.build(override=False, hero=True, width=100, props={"height": 200}) # override not expected
    @layout(hero=False, width=100, props={"height": 200})
    @Airway.layout(override=True, width=100, props={"height": 200})
    def my_func():
        pass

    
    res0 = layout(my_func) # same as @layout/my_func (must be recorded)
    assert res0 == my_func
    res1 = Airway.build(my_func) # same as @build/my_func (must be recorded)
    assert res1 == my_func
    
    res2 = layout(my_func, override=True, role="user")
    assert res2.get("func", "not there") == my_func
    assert res2.get("props", "not there") == {"role":"user"}
    assert res2.get("layout_override", "not there") is True
    assert res2.get("layout_hero", "not there") == None
    
    
    res3 = build(True, my_func, role="user")
    assert res3.get("func", "not there") == my_func
    assert res3.get("props", "not there") == {"role":"user"}
    assert res3.get("build_hero", "not there") is True
    
    res4 = Airway('home').layout(override=False).build(my_func).build(hero=True).layout(my_func).fly_in(my_func).fly_in(my_func)
    res4.fly_in(my_func, apply_per_view=True, override=True, props={"a":1}, b=2)
    assert isinstance(res4, Airway)
    assert res4._build["func"]==my_func
    assert res4._layout["func"]==my_func
    assert res4.fly_ins[0]["func"]==my_func
    assert res4.fly_ins[0]["props"]=={}
    assert res4.fly_ins[0]["inheritable"]==True
    assert res4.fly_ins[0]["apply_per_view"]==False
    assert res4.fly_ins[1]["func"]==my_func
    assert res4.fly_ins[1]["props"]=={}
    assert res4.fly_ins[1]["inheritable"]==True
    assert res4.fly_ins[1]["apply_per_view"]==False
    assert res4.fly_ins[2]["func"]==my_func
    assert res4.fly_ins[2]["props"]=={'a':1, 'b':2}
    assert res4.fly_ins[2]["inheritable"]==True
    assert res4.fly_ins[2]["apply_per_view"]==True
    assert res4.fly_in_override == True
    assert res4.layout_override == False
    assert res4.layout_hero == None
    assert res4.build_hero == True


    layout_list = getattr(my_func, "_fletfly_layout", {})

    assert len(layout_list) == 3

    assert layout_list[0].get("props", {}).get("height", None) == 200
    assert layout_list[0].get("props", {}).get("width", None) == 100
    assert layout_list[0].get("layout_override", "not there") is True
    assert layout_list[0].get("layout_hero", "not there") == "not there"

    assert layout_list[1].get("props", {}).get("height", None) == 200
    assert layout_list[1].get("props", {}).get("width", None) == 100
    assert layout_list[1].get("layout_override", "not there") == "not there"
    assert layout_list[1].get("layout_hero", "not there") is False

    build_list = getattr(my_func, "_fletfly_build", {})

    assert len(build_list) == 3

    assert build_list[0].get("props", {}).get("height", None) == 200
    assert build_list[0].get("props", {}).get("width", None) == 100
    assert build_list[0].get("props", {}).get("override", None) is False
    assert build_list[0].get("build_override", "not there") == "not there"
    assert build_list[0].get("build_hero", "not there") is True

    assert build_list[1].get("props", {}).get("height", None) == 200
    assert build_list[1].get("props", {}).get("width", None) == 100
    assert build_list[1].get("props", {}).get("override", None) is False
    assert build_list[1].get("build_override", "not there") == "not there"
    assert build_list[1].get("build_hero", "not there") == "not there"

    fly_in_list = getattr(my_func, "_fletfly_fly_in", {})
    assert len(fly_in_list) == 2

    assert fly_in_list[0].get("props", {}).get("height", None) == 200
    assert fly_in_list[0].get("props", {}).get("width", None) == 100
    assert fly_in_list[0].get("fly_in_override", "not there") == False
    assert fly_in_list[0].get("apply_per_view", "not there") is False
    assert fly_in_list[0].get("inheritable", "not there") is True

    assert fly_in_list[1].get("props", {}).get("height", None) == 200
    assert fly_in_list[1].get("props", {}).get("width", None) == 100
    assert fly_in_list[1].get("fly_in_override", "not there") == False
    assert fly_in_list[1].get("apply_per_view", "not there") is True
    assert fly_in_list[1].get("inheritable", "not there") is True
    
    fly_out_list = getattr(my_func, "_fletfly_fly_out", {})
    assert len(fly_out_list) == 2

    assert fly_out_list[0].get("props", {}).get("height", None) == 200
    assert fly_out_list[0].get("props", {}).get("width", None) == 100
    assert fly_out_list[0].get("fly_out_override", "not there") == False
    assert fly_out_list[0].get("apply_per_view", "not there") is False
    assert fly_out_list[0].get("inheritable", "not there") is False

    assert fly_out_list[1].get("props", "not there") == {}
    assert fly_out_list[1].get("fly_out_override", "not there") == "not there"
    assert fly_out_list[1].get("apply_per_view", "not there") is False
    assert fly_out_list[1].get("inheritable", "not there") is False
    
def test_subway_func_inject():
    aw = Airway()
    @subway
    @Airway.subway(path='third', hero=True, width=100, props={"height": 200}) # override not expected
    @subway(path='second', fly_to="/", width=100, props={"height": 200})
    @Airway.subway(path='first', width=100, props={"height": 200})
    def my_func():
        pass

    res0 = subway(my_func) # same as @subway/my_func (must be recorded)
    assert res0 == my_func
    res1 = Airway.subway(my_func) # same as @Airway.subway/my_func (must be recorded)
    assert res1 == my_func 
    
    res2 = Airway("home", role = "admin")
    res3 = res2.subway("settings", role = "user")
    assert res2.path == "home"
    assert res2.props.get("role", "not there") == "admin"
    assert res2.subways[0] == res3
    assert res3.path == "settings"
    assert res3.props.get("role", "not there") == "user"
    
    res4 = res2.subway(my_func, "settings", role="user")
    assert res4.path == "settings"
    assert res4._build["func"] == my_func
    assert res4._build["props"]["role"] == "user"
        
    res5 = Airway.subway("settings", my_func, role="user")
    assert res5.path == "settings"
    assert res5._build["func"] == my_func
    assert res5._build["props"]["role"] == "user"
        

    res6 = getattr(my_func, "_fletfly_subway", [])
    
    assert len(res6) == 6
    assert res6[0].get("path", "not there") == "first"
    assert res6[0].get("fly_to", "not there") == "not there"
    assert res6[0].get("props",{}).get("width") == 100
    assert res6[0].get("props",{}).get("height") == 200
    
    assert res6[1].get("path", "not there") == "second"
    assert res6[1].get("fly_to", "not there") == "/"
    assert res6[1].get("props",{}).get("width") == 100
    assert res6[1].get("props",{}).get("height") == 200
    
    assert res6[2].get("path", "not there") == "third"
    assert res6[2].get("fly_to", "not there") == "not there"
    assert res6[2].get("props",{}).get("width") == 100
    assert res6[2].get("props",{}).get("height") == 200
    
    assert res6[3].get("path", "not there") == "not there"
    assert res6[3].get("fly_to", "not there") == "not there"
    assert res6[3].get("props", "not there") == {}
    
def test_inject_class():
    @fly_out
    @fly_out(override=False, apply_per_view=False, width=100, props={"height":200}) # inheritable has a default = True    
    @fly_in(override=False, apply_per_view=True, width=100, props={"height":200}) # inheritable has a default = True
    @fly_in(override=False, apply_per_view=False, width=100, props={"height":200}) # inheritable has a default = True
    @build(override=False, width=100, props={"height": 200}) # override not expected
    @Airway.build(override=False, hero=True, width=100, props={"height": 200}) # override not expected
    @layout(hero=False, width=100, props={"height": 200})
    @Airway.layout(override=True, width=100, props={"height": 200})
    class MyClass:
        pass

    
    res0 = layout(MyClass) # same as @layout/my_func (must be recorded)
    assert res0 == MyClass
    res1 = Airway.build(MyClass) # same as @build/my_func (must be recorded)
    assert res1 == MyClass
    
    res2 = layout(MyClass, override=True, role="user")
    
    assert res2.get("func", "not there") == MyClass
    assert res2.get("props", "not there") == {"role":"user"}
    assert res2.get("layout_override", "not there") is True
    assert res2.get("layout_hero", "not there") == None
    
    
    res3 = build(True, MyClass, role="user")
    assert res3.get("func", "not there") == MyClass
    assert res3.get("props", "not there") == {"role":"user"}
    assert res3.get("build_hero", "not there") is True
    
    res4 = Airway('home').layout(override=False).build(MyClass).build(hero=True).layout(MyClass).fly_in(MyClass).fly_in(MyClass)
    res4.fly_in(MyClass, apply_per_view=True, override=True, props={"a":1}, b=2)
    assert isinstance(res4, Airway)
    assert res4._build["func"]==MyClass
    assert res4._layout["func"]==MyClass
    assert res4.fly_ins[0]["func"]==MyClass
    assert res4.fly_ins[0]["props"]=={}
    assert res4.fly_ins[0]["inheritable"]==True
    assert res4.fly_ins[0]["apply_per_view"]==False
    assert res4.fly_ins[1]["func"]==MyClass
    assert res4.fly_ins[1]["props"]=={}
    assert res4.fly_ins[1]["inheritable"]==True
    assert res4.fly_ins[1]["apply_per_view"]==False
    assert res4.fly_ins[2]["func"]==MyClass
    assert res4.fly_ins[2]["props"]=={'a':1, 'b':2}
    assert res4.fly_ins[2]["inheritable"]==True
    assert res4.fly_ins[2]["apply_per_view"]==True
    assert res4.fly_in_override == True
    assert res4.layout_override == False
    assert res4.layout_hero == None
    assert res4.build_hero == True


    layout_list = getattr(MyClass, "_fletfly_layout", {})

    assert len(layout_list) == 3

    assert layout_list[0].get("props", {}).get("height", None) == 200
    assert layout_list[0].get("props", {}).get("width", None) == 100
    assert layout_list[0].get("layout_override", "not there") is True
    assert layout_list[0].get("layout_hero", "not there") == "not there"

    assert layout_list[1].get("props", {}).get("height", None) == 200
    assert layout_list[1].get("props", {}).get("width", None) == 100
    assert layout_list[1].get("layout_override", "not there") == "not there"
    assert layout_list[1].get("layout_hero", "not there") is False

    build_list = getattr(MyClass, "_fletfly_build", {})

    assert len(build_list) == 3

    assert build_list[0].get("props", {}).get("height", None) == 200
    assert build_list[0].get("props", {}).get("width", None) == 100
    assert build_list[0].get("props", {}).get("override", None) is False
    assert build_list[0].get("build_override", "not there") == "not there"
    assert build_list[0].get("build_hero", "not there") is True

    assert build_list[1].get("props", {}).get("height", None) == 200
    assert build_list[1].get("props", {}).get("width", None) == 100
    assert build_list[1].get("props", {}).get("override", None) is False
    assert build_list[1].get("build_override", "not there") == "not there"
    assert build_list[1].get("build_hero", "not there") == "not there"

    fly_in_list = getattr(MyClass, "_fletfly_fly_in", {})
    assert len(fly_in_list) == 2

    assert fly_in_list[0].get("props", {}).get("height", None) == 200
    assert fly_in_list[0].get("props", {}).get("width", None) == 100
    assert fly_in_list[0].get("fly_in_override", "not there") == False
    assert fly_in_list[0].get("apply_per_view", "not there") is False
    assert fly_in_list[0].get("inheritable", "not there") is True

    assert fly_in_list[1].get("props", {}).get("height", None) == 200
    assert fly_in_list[1].get("props", {}).get("width", None) == 100
    assert fly_in_list[1].get("fly_in_override", "not there") == False
    assert fly_in_list[1].get("apply_per_view", "not there") is True
    assert fly_in_list[1].get("inheritable", "not there") is True
    
    fly_out_list = getattr(MyClass, "_fletfly_fly_out", {})
    assert len(fly_out_list) == 2

    assert fly_out_list[0].get("props", {}).get("height", None) == 200
    assert fly_out_list[0].get("props", {}).get("width", None) == 100
    assert fly_out_list[0].get("fly_out_override", "not there") == False
    assert fly_out_list[0].get("apply_per_view", "not there") is False
    assert fly_out_list[0].get("inheritable", "not there") is False

    assert fly_out_list[1].get("props", "not there") == {}
    assert fly_out_list[1].get("fly_out_override", "not there") == "not there"
    assert fly_out_list[1].get("apply_per_view", "not there") is False
    assert fly_out_list[1].get("inheritable", "not there") is False