import asyncio
import flet as ft
from fletfly import Route, slot, fly, fly_in, child

class Home(Route):             # Route detection: path auto named to "/home"
    def layout(self, page):    # Auto-detected layout
        return ft.Column([
                ft.Text("Header"),
                slot(page) ])  # Nameless slot for injection
            
    @classmethod
    def fly_in(cls):           # Middleware
        return True
    
    @staticmethod               
    def contact():               # Sub route(method), named to "/home/contact"
        return ft.Text("Contact page")      # injected into self layout
    
    class User:                # Sub route(class), named to "/home/user"
        @classmethod
        def view(cls):         # main view detection, into layout inject
            return ft.Text('User page')     # injected into parent layout
    
    @child('about', value='About page')     # fast route "/home/about"
    @child('error', value='Error page')     # fast route "/home/error"
    class A(ft.Text): pass



async def main(page):
    fly(page)

    target_pages = ["home/contact", "home/user", "home/about", 'home/error']
    for p in target_pages:
        await asyncio.sleep(5)
        page.fly(p)

ft.run(main)