
import flet as ft
import fletfly as fty
from fletfly import Route, General, General, fly


@Route('home1')
class page1:
    pass
    class page11(Route): pass

@Route()
class page2:
    route = ""
    def element(page):
        return ft.Text("Home")
    class page21(Route): pass


def parent(cls):
    cls.parent = "Mohab"
    return cls
def brother(cls):
    cls.brother = "Amer"
    return cls

@Route
class page3:
    route = "/home3" 
    def layout(page):
        return ft.Column([
            ft.Text("HHHHHHHHHHHHHHHH"),
            fty.slot(page),
            ft.Text("FFFFFFFFFFFFFFFF")
        ])
    
    def view(page):
        return ft.Text("home3")
    def page31(page):
        return ft.Text("page 31, A func in the class, returning ft.Control, we'll treat it as a page")
    def page32(page):
        return ft.Text("page 32, fast page, nothing but path, view & ref to the class")
home = Route("home1/home4")
@home
class page4: pass

home = Route()
@home("/home1/home888/home999/home5")
class page5:
    class page51:
        url = "home51"
        class page5:
            path = "home511"
    class page52:
        pass
        class page5(Route):
            path = "525"

class page6(Route):
    route = "/home1/home888"

@Route("/home1/home888/home999")
class page7(Route):
    def view(page):
        return ft.Text("home1/home888/home999")

class page8(Route):
    path = "/:name/[age]/{address}"
    def view(page):
        return ft.Text(f"This is home999 of {page.fly.params.get("name", "No one")}")
    class page81: pass
class page9(Route):
    url = "/home9"
    class page91():
        url = "home91"
        class page911():
            path = "home911"
    class page92:
        url = "home92"
        class page921:
            path = "home921"
    class page93:
        url = "home93"
        class page931(page1, page2, page3):
            path = "home931"
    children = [page6, page7, page8]
page9.children.append(page8)

class page0(Route):
    def layout(page):
        return ft.Column([
            ft.Text("This is a nice header"),
            ft.Text("this is a very nice header"),
            fty.slot(page),
            ft.Text("This is a footer"),
            ft.Text("this is a very nice footer"),
        ])
    def view(page):
        return ft.Text("This is Page20 Class")
    
    class page01:
        def layout(page):
            return ft.Column([ft.Text("21 21 21 21 21 21"),
                              fty.slot(page),
                              ft.Text("21 21 21 21 21 21")
            ])
        def view(page):
            return ft.Text("This is page21")
        class page1:
            layout_override = True
            def view(page):
                return ft.Text("This is page 1")
    class page02:
        pass
        class page1: pass


"""
weird = [
    {"path":"page77", "component":lambda p:ft.Text("hi"), "children":[
        {"path":"page101", "component":None},
        {"path":"page102", "compoentn":None},
        #{"path":":id", "view":lambda:ft.Text("hello")},
        #{"url":"[name]", "content": lambda: ft.Text("see you")}

    ]},
    {"page76":lambda p:ft.Text("bye")},


    Route("mohab", land=None, children=[
        Route("Bilal", land=None),
        Route("Omar", land=None, children=[
            Route("salem", land=None)

    ])])]
    
"""

def mw_son(must_arg1, must_arg2, optional_arg1 = "default optional_arg1", optional_arg2 = "default optional_arg2"):
    print("🔐 [MW 1] Checking son...")
    print("must_arg1:", must_arg1)
    print("must_arg2:", must_arg2)
    print("optional_arg1:", optional_arg1)
    print("optional_arg2:", optional_arg2)
    print("injected page is working:", fty.page)
    print("injected route is working:", fty.route)
    print("injected is_final is working:", fty.is_final)
    return True

def mw_auth(must_arg1, must_arg2, optional_arg1 = "default optional_arg1", optional_arg2 = "default optional_arg2"):
    print("🔐 [MW 2] Checking Auth...")
    print("must_arg1:", must_arg1)
    print("must_arg2:", must_arg2)
    print("optional_arg1:", optional_arg1)
    print("optional_arg2:", optional_arg2)
    print("injected page is working:", fty.page)
    print("injected route is working:", fty.route)
    print("injected is_final is working:", fty.is_final)
    return True


def mw_role(must_arg1, must_arg2, optional_arg1 = "default optional_arg1", optional_arg2 = "default optional_arg2"):
    print("🔐 [MW 3] Checking Role...")
    print("must_arg1:", must_arg1)
    print("must_arg2:", must_arg2)
    print("optional_arg1:", optional_arg1)
    print("optional_arg2:", optional_arg2)
    print("injected page is working:", fty.page)
    print("injected route is working:", fty.route)
    print("injected is_final is working:", fty.is_final)
    return True
# --- تجربة الـ Nesting في الخريطة (Static Map) ---
"""
Pages = {
    "/": lambda p: ft.Text("Home Page"),
    
    # هنا اللحظة الحاسمة: ميدل وير مغلف ميدل وير تاني
    "admin":
        (fty.fly_in(mw_role, 1, 2, 3, apply_per_view=True)(
        fty.fly_in(mw_auth, 11, 12, optional_arg2 = "14")(
            {
            "": lambda p: ft.Text("Admin Dashboard"),
            "settings": fty.fly_in(mw_son, 21, 22)( lambda p: ft.Text("Admin Settings")),
            "overrided": fty.fly_in(override=True)(lambda p: ft.Text("page1 overrided")),
            }
        ))),
    "page1": fty.fly_in([
        (mw_auth, 101, 102, 103),
        (mw_role, 104, 105, 106, 107),
        (mw_son, 104, 105, 106, 107),
        ])({
            "": lambda p: ft.Text("This is PAGE1"),
            "settings": lambda p: ft.Text("page1 Settings"),
            "overrided": fty.fly_in(override=True)(lambda p: ft.Text("page1 overrided")),
                              }),
    "error": lambda p: ft.Text("Error")
}

"""
ft.run(fly)
