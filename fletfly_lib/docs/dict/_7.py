import flet as ft
import fletfly as fy 

def check_role(role='user'):          # general middleware with params
    return True if role == 'admin' else 'home'
    
def home_view(): 
    return ft.Text("Main view")

def admin_view(): 
    return ft.Text("Admin view")

def fly_in_self(): 
    return True

def func(param1):
    return True

home = {
    "path": "home",
    "view": home_view,
    "children": [
        {
            "path": "admin",          # Sub route, path: "/home/admin"
            "view": admin_view,
            "fly_in_override": True,  # Overriding parent middlewares
            "fly_ins": [
                (func, {"inheritable": True, "param1": "a"}), # Inheritable middleware with props via tuple
                (check_role, {"role": "user"}),               # External function with parameters via tuple
                fly_in_self                                   # Local middleware callable directly
            ]
        }
    ]
}

fy.Router(home)

def main(page):
    fy.fly(page, '/home/admin')

ft.run(main=main)