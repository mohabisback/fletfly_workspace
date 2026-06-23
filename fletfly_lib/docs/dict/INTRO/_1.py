import asyncio
import flet as ft
import fletfly as fy

def layout(page):
    return ft.Column([
        ft.Text("Header"),
        fy.slot(page)
    ])

def fly_in_middleware():
    return True

def contact_view():
    return ft.Text("Contact page")

def user_view():
    return ft.Text('User page')

def text(value=''):
    return ft.Text(value)
# Wrap(decorate) your dict with Route() for:
home = fy.Route({           # Auto detection and insertion into routes tree
    "path": None,           # auto-path naming to: '/home'
    "layout": layout,
    "fly_in": fly_in_middleware,
    "children": [
        {"path": "contact", "view": contact_view},
        {"path": "user", "view": user_view},
        {"path": "about", "view": text, "props": {"value": "About page"}},
        {"path": "error", "view": lambda: ft.Text("Error page")}
    ]
})

async def main(page):
    fy.fly(page)
    target_pages = ["home/contact", "home/user", "home/about", 'home/error']
    for p in target_pages:
        await asyncio.sleep(2)
        page.fly(p)

ft.run(main)