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

# Declarative tree composition
home = fy.Route(
    fy.use.view(home_view),
    children=[
        # Child route with fly_in_override passed directly via kwargs props
        fy.Route('admin', 
            fy.use.view(admin_view),
            fly_in_override=True,
            fly_ins = [
                fy.use.fly_in(func, inheritable=True, param1='a'), # Registering inheritable middleware with props
                fy.use.fly_in(check_role, role='user'),             # Registering external function to fly_in explicitly with parameters (change role to "admin", to enter the page)
                fly_in_self
                ],                        # Registering local middleware explicitly
        )
    ]
)

def main(page):
    fy.fly(page, '/home/admin')

ft.run(main=main)