# main.py file of master project
import flet as ft
from fletfly import Route, Zone, fly
from fletfly.docs.class.INTRO.b10_zone import Home as Project1

class Home(Route): # Main project
    path = '/home'
    def view(self, page): return ft.Button("Go Project", on_click=lambda e: e.page.fly('home/project'))
    Project = Zone(Project1) # Zone

ft.run(fly)