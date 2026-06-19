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

# Declarative tree composition
home = fy.Route('home', fy.use.layout(layout), fy.use.fly_in(fly_in_middleware),
    children=[
        fy.Route('contact', contact_view),
        fy.Route('user', user_view),
        fy.Route('about', fy.use.view(text, value ="About page")),
        fy.Route('error', fy.use.view(lambda: ft.Text("Error page")))
    ]
)

async def main(page):
    fy.fly(page)

    target_pages = ["home/contact", "home/user", "home/about", 'home/error']
    for p in target_pages:
        await asyncio.sleep(5)
        page.fly(p)

ft.run(main)