import asyncio
import flet as ft
import fletfly as fy

class Home(fy.Route):             # Route detection: path auto named to "/home"
    def layout(self, page):    # Auto-detected layout
        return ft.Column([
                ft.Text("Header"),
                fy.slot(page) ])  # Nameless slot for injection
            
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
    
    @fy.child('about', value='About page')     # fast route "/home/about"
    @fy.child('error', value='Error page')     # fast route "/home/error"
    class A(ft.Text): pass

async def main(page):
    fy.fly(page)

    target_pages = ["home/contact", "home/user", "home/about", 'home/error']
    for p in target_pages:
        await asyncio.sleep(2)
        fy.fly(page, p)

ft.run(main)