import flet as ft
def get_view(page):

    view = ft.View(
        appbar=ft.AppBar(title=ft.Text("Path Error"), bgcolor="red"),
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Icon(ft.Icons.ERROR_OUTLINE, color="red", size=100),
            ft.Text("Sorry, Page doesn't exist", size=30, weight="bold"),
            ft.Button("Back home", on_click= lambda _: page.fly("/"))
        ]
    )
    return view