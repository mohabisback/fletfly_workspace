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

# Route instance initialization with kwargs props
profile = fy.Route('profile/:id',
                layout= fy.use.layout(layout),
                fly_ins=[fy.use.fly_in(external_func, auth=True)], # Registering external function to fly_in explicitly
                view=fy.use.view(view),
                role='admin', theme='dark', props={'num':3},
)

def main(page):
    fy.fly(page, 'profile/fletfly')

ft.run(main)