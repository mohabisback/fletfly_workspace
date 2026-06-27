import asyncio
import flet as ft
import fletfly as fy

home = fy.Route()                          # Route detection: path auto named to "/home"

@home.use.layout
def layout(page):                       # Auto-detected layout
    return ft.Column([
            ft.Text("Header"),
            fy.slot(page) ])               # Nameless slot for injection
            
@home.use.fly_in
def fly_in():                           # Middleware
    return True

@home.use.child('contact')
def contact():                          # subroute from func, named to "/home/contact"
    return ft.Text("Contact page")      # injected into self layout

@home.use.child('about', value='About page')     # fast route "/home/about"
@home.use.child('error', value='Error page')     # fast route "/home/error"
class A(ft.Text): pass

user = fy.Route('user')                            # Subroute, named to "/home/user"
@user.use.view
def view():                         # main view detection, into layout inject
    return ft.Text('User page')     # injected into parent layout

home.children.append(user)

async def main(page):
    fy.fly(page)

    target_pages = ["home/contact", "home/user", "home/about", 'home/error']
    for p in target_pages:
        await asyncio.sleep(2)
        fy.fly(page, p)

ft.run(main)