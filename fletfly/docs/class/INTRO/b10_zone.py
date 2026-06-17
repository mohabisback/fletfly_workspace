# main.py of sub project
import flet as ft
from fletfly import Route, fly

class Home(Route):
    path = '/home'
    def view(self, page):
        return ft.Column([
            ft.Text ("Sub project Home page"),
            ft.Button('Go settings', on_click=lambda e: e.page.fly('home/settings'))
        ])
    class Settings:
        path = '/home/settings'
        def view(self, page):
            return ft.Column([
                ft.Text ("Sub project Settings page"),
                ft.Button('Go Home', on_click=lambda e: e.page.fly('home'))
            ])
if __name__ == "__main__":
    ft.run(fly)