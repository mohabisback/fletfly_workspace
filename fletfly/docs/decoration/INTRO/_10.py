import flet as ft
import fletfly as fy

def external_func(auth=False):
    print("Middleware check passed")
    return auth

# Route instance initialization with kwargs props
profile = fy.Route('profile/:id', role='admin', theme='dark', props={'num':3})

@profile.use.layout
def layout(page, theme): 
    # Layout only requests 'theme' from route props
    return ft.Column([
        ft.Text(f"Theme: {theme}"),
        fy.slot(page)
    ])

# Registering external function to fly_in explicitly
profile.fly_ins.append(fy.Route.fly_in(external_func, auth=True))
# or
profile.use.fly_in(auth=True)(external_func) # decoration immitation

@profile.use.view
def view(id, role, num): 
    # View requests 'id' (dynamic param) and 'role'/'num' (route props)
    return ft.Text(f"User {id} with number {num} is logged in as {role}")

def main(page):
    fy.fly(page, 'profile/fletfly')

ft.run(main)