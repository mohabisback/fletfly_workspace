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

# Chaining style composition
home = fy.Route().layout(layout).fly_in(fly_in_middleware)

contact = home.child().view(contact_view) # auto named
user = home.child().view(user_view)
about = home.child().view(text, value="About page")

home.child('error').view(lambda: ft.Text("Error page"))

async def main(page):
    fy.fly(page)
    target_pages = ["home/contact", "home/user", "home/about", 'home/error']
    for p in target_pages:
        await asyncio.sleep(2)
        page.fly(p)

ft.run(main)