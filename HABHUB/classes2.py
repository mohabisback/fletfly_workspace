import flet as ft
import fletfly as fty
from fletfly import Route, General, General, fly, layout


route = Route('/home')
@Route()
class A:

    @layout(True, True)
    def func_name(page):
        return ft.Text("Layout")
    
    if hasattr(func_name, "_fletfly_layout"):
        print(2222222, "_fletfly_layout:", func_name._fletfly_layout)
    else:
        print(222222, "_fletfly_layout:", "N/A")

    if hasattr(func_name, "_fletfly_layout_hero"):
        print(3333333, "_fletfly_layout_hero:", func_name._fletfly_layout_hero)
    else:
        print(3333333, "_fletfly_layout_hero:", "N/A")

    if hasattr(func_name, "_fletfly_layout_override"):
        print(4444444, "_fletfly_layout_override:", func_name._fletfly_layout_override)
    else:
        print(4444444, "_fletfly_layout_override:", "N/A")
    
    print(000000000, "route._layout", route._layout)
    print(555555555, "route.layout", route.layout)
    print(666666666, "route.layout_clsattr", route.layout_clsattr)
    print(777777777, "route.layout_hero", route.layout_hero)
    print(888888888, "route.layout_override", route.layout_override)


ft.run(fly)