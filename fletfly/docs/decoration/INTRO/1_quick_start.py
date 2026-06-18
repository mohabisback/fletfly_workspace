import asyncio
import flet as ft
from fletfly import Route, slot, fly

home = Route()                          # Route detection: path auto named to "/home"

@home.at.layout
def layout(page):                       # Auto-detected layout
    return ft.Column([
            ft.Text("Header"),
            slot(page) ])               # Nameless slot for injection
            
@home.at.fly_in
def fly_in():                           # Middleware
    return True

@home.at.child('contact')
def contact():                          # subroute from func, named to "/home/contact"
    return ft.Text("Contact page")      # injected into self layout

@home.at.child('about', value='About page')     # fast route "/home/about"
@home.at.child('error', value='Error page')     # fast route "/home/error"
class A(ft.Text): pass

user = Route('user')                            # Subroute, named to "/home/user"
@user.at.view
def view():                         # main view detection, into layout inject
    return ft.Text('User page')     # injected into parent layout

home.children.append(user)

async def main(page):
    fly(page)

    target_pages = ["home/contact", "home/user", "home/about", 'home/error']
    for p in target_pages:
        await asyncio.sleep(5)
        page.fly(p)

ft.run(main)