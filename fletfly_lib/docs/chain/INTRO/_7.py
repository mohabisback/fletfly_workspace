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

# Chaining style composition
home = fy.Route().view(home_view)

# Child route with fly_in_override passed directly via kwargs props
home.child('admin', fly_in_override=True).view(admin_view)\
    .fly_in(func, inheritable=True, param1='a')\
    .fly_in(check_role, role='user')\
    .fly_in(fly_in_self)

def main(page):
    fy.fly(page, '/home/admin')

ft.run(main=main)