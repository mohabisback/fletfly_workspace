import flet as ft
from fletfly import Route, slot, fly
class Home(Route):
    path = "{category}"               # dynamic page
    layout_hero = False               # layout deleted once no view uses it(default)
    def layout(self, page):           
        return ft.Column([
            ft.Text("Header"),
            slot(page)
            ])
    view_hero = True                  # True means 5 in dynamic, 1 in static
    def view(self):
        return ft.Text("Main view")
    class User:
        path = ":id"                  # dynamic page
        view_hero = 2                 # max 2 pages are saved for different params
        def view(self, id):
            return ft.Text(f"page: {id}")
ft.run(fly)