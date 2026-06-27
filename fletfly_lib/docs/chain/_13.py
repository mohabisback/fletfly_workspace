import flet as ft
import fletfly as fy

class User(fy.Route):
    @fy.child(':id')
    def view(self, id, profile=None, color=None): # 1-through parameters
        return ft.Column([
            ft.Text(f"Argument id: {id}"),
            ft.Text(f"Argument profile: {profile}"),
            ft.Text(f"Argument color: {color}"),
            # 2-through fy.fly(page).params or fy.fly(page).query
            ft.Button("Print fly(page).", on_click=lambda e: print(
                "fly(page).params.get('id'):", fy.fly(e.page).params.get("id"), '\n'
                "fly(page).query.get('profile'):", fy.fly(e.page).query.get("profile"), '\n'
                "fly(page).query.get('color'):", fy.fly(e.page).query.get("color"), '\n'
            )),
            # 3-through page.fly.params or page.fly.query
            ft.Button("Print page.fly.", on_click=lambda e: print(
                "page.fly.params.get('id'):", e.page.fly.params.get("id"), '\n'
                "page.fly.query.get('profile'):", e.page.fly.query.get("profile"), '\n'
                "page.fly.query.get('color'):", e.page.fly.query.get("color"), '\n'
            )),
        ])

def main(page):
    fy.fly(page, 'user/101?profile=premium&color=red')

ft.run(main)