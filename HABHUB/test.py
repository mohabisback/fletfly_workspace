import flet as ft
import fletfly as fty
from fletfly import Airway, fly

@Airway('/home1')
class page1: 
    pass
    class page1(Airway): pass

@Airway()
class page2:
    route = "/home2"
    class page1(Airway): pass
@Airway
class page3:
    route = "/home3"

home = Airway("/home4")
@home
class page4: pass

home = Airway()
@home("/home5")
class page5:
    class page51:
        url = "home51"
        class page5:
            path = "home511"
    class page52:
        pass
        class page5(Airway):
            path = "525"

@fly
class page6:
    route = "/home6"

@fly("/home7")
class page7: pass

class page8(Airway):
    path = "/home8"
    class page81: pass
class page9(Airway):
    url = "/home9"
    class page91:
        url = "home91"
        class page911:
            path = "home911"
    class page92:
        url = "home93"
        class page921:
            path = "home921"
    class page93:
        url = "home93"
        class page931:
            path = "home931"

class page20:
    pass
    
    class page21:
        class page1: pass
        pass
    class page22:
        pass
        class page1: pass
    class page23:
        pass
        class page1: pass


weird = [
    {"path":"page77", "component":lambda:ft.Text("hi"), "children":[
        {"path":"page101", "component":None},
        {"path":"page102", "compoentn":None},
        #{"path":":id", "view":lambda:ft.Text("hello")},
        #{"url":"[name]", "content": lambda: ft.Text("see you")}

    ]},
    {"page76":lambda:ft.Text("bye")},


    Airway("mohab", land=None, subways=[
        Airway("Bilal", land=None),
        Airway("Omar", land=None, subways=[
            Airway("salem", land=None)

    ])])]
    

airline = fty.Airline([page20, weird])



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
# 3. التشغيل
def main(page: ft.Page):
    fly(page)

if __name__ == "__main__":
    ft.run(main)
