import flet as ft
from fletfly import Router, Route, slot, fly, Shared, view


class Home(Route):
    def layout(self, page):
        return ft.Column([
            slot(page, 'A', shared=True),
            slot(page, 'named class', shared=True),
            slot(page, 'function not method', shared=True),
            slot(page, 'two', shared=True),
            slot(page, 'another function', shared=True),
            slot(page, 'named func', shared=True),
            slot(page, 'class as view', shared=True),
            slot(page, 'class as view1', shared=True),
            slot(page, 'class as view2', shared=True),
            slot(page, 'class as view3', shared=True),
            slot(page, 'class as view4', shared=True),
            slot(page, 'E', shared=True),
            slot(page, 'C', shared=True),
        ])

@Shared
class A:
    def view(self):
        return ft.Text("Shared A")

@Shared('named class')
class B:
    @Shared('function not method', props={'self':None})
    def view(self):
        return ft.Text("Shared B")
    @Shared(props={'self':None})
    def two(self):
        return ft.Text("shared two")
@Shared
def C():
    return ft.Text("Shared C")

@Shared('named func')
def D():
    return ft.Text("Shared D")

class E: 
    def view(self):
        return ft.Text("Class E")
@Shared('class as view')
class F(ft.Text):
    @Shared.view(value="This is the orignal decoration procedure")
    class G(ft.Text):
        pass

Shared(E)
Shared('another function', C)
Shared('class as view1', (F, {"value":"This is a class inherited from ft.Text"}))
Shared('class as view2', Shared.view(F, value="2222 This is a class inherited from ft.Text"))
Shared('class as view3').view(F, value='This is a class acting as a view')
Shared('class as view4').view = view(F, value="2222 This is a class inherited from ft.Text")

Router(print_shared_views=True)
ft.run(fly)