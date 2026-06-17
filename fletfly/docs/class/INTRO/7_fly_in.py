import flet as ft
from fletfly import Route, fly, fly_in

def check_role(role='user'):          # general middleware with params
    return True if role == 'admin' else 'home'
    
class Home(Route):
    def view(self): return ft.Text("Main view")
    
    class Admin:
        def view(self): return ft.Text("Admin view")
        fly_in_override = True     # overrides all parent inheritable middlewares
        def fly_in_self(self): # middleware, detected by name
            return True
        
        @classmethod               
        @fly_in(inheritable = True, param1='a') # detected by decoration
        def func(cls, param1):
            return True

        d = fly_in(check_role, role='user')  # change role to "admin", to enter the page

def main(page):
    fly(page, '/home/admin')
ft.run(main)