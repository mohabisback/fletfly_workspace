import flet as ft
from fletfly import Route, fly, slot

def external_func(auth=False):
    print("Middleware check passed")
    return auth

@Route('profile/:id', role='admin', theme='dark', props={'num':3}) # Route props via **kwargs
class Profile:
    # Layout only requests 'theme' from route props
    def layout(self, page, theme): 
        return ft.Column([
            ft.Text(f"Theme: {theme}"),
            slot(page)
        ])
    fly_in = Route.fly_in(external_func, auth=True) # specific props
    # View requests 'id' (dynamic param) and 'role' (route prop)
    def view(self, id, role, num): 
        return ft.Text(f"User {id} with number {num} is logged in as {role}")
def main(page):
    fly(page, 'profile/fletfly')
ft.run(main)