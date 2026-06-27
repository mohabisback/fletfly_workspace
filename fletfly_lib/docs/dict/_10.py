import flet as ft
import fletfly as fy

def external_func(auth=False):
    print("Middleware check passed")
    return auth

def layout(page, theme): 
    # Layout only requests 'theme' from route props
    return ft.Column([
        ft.Text(f"Theme: {theme}"),
        fy.slot(page)
    ])

def view(id, role, num): 
    # View requests 'id' (dynamic param) and 'role'/'num' (route props)
    return ft.Text(f"User {id} with number {num} is logged in as {role}")

# Dict registration mode conversion
profile = {
    "path": "profile/:id",
    "layout": layout,
    "view": view,
    "fly_ins": [
        (external_func, {"auth": True})  # Explicit middleware with parameters via tuple
    ],
    "role": "admin",     # Auto collected prop
    "theme": "dark",     # Auto collected prop
    "props": {"num": 3}  # Explicit props
}

# Initializing the Router with the configuration tree
fy.Router(profile)

async def main(page):
    fy.fly(page, 'profile/fletfly')

ft.run(main=main)