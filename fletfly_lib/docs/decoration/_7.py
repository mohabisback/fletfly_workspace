import flet as ft
import fletfly as fy 

def check_role(role='user'):          # general middleware with params
    return True if role == 'admin' else 'home'
    
home = fy.Route()

@home.use.view
def home_view(): 
    return ft.Text("Main view")

# Child route with fly_in_override passed directly via kwargs props
admin = fy.Route('admin', fly_in_override=True)

@admin.use.view
def admin_view(): 
    return ft.Text("Admin view")

# Registering local middleware explicitly
@admin.use.fly_in
def fly_in_self(): 
    return True

# Registering inheritable middleware with props
@admin.use.fly_in(inheritable=True, param1='a')
def func(param1):
    return True

# Registering external function to fly_in explicitly with parameters
admin.use.fly_in(role='user')(check_role)  # change role to "admin", to enter the page

home.children.append(admin)

def main(page):
    fy.fly(page, '/home/admin')

ft.run(main=main)