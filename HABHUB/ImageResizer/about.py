#ImageResizer/about.py
import flet as ft
def get_view(page):
    def open_home(e):
        page.fly("/")

    view = ft.View(
        appbar=ft.AppBar(title=ft.Text("About Resizer")),
        controls=[
            ft.Text("This module handles image processing.", size=20),
            ft.Button("Home", on_click=open_home)
        ]
    )

    return view