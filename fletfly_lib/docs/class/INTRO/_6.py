import asyncio
import flet as ft
import fletfly as fy

class Home(fy.Route):
    def layout(self, page):
        return ft.Column([
            ft.Text('Header'),
            fy.slot(page)
        ])
    # @child(layout_override=True)     # decoration on class can work
    class Settings:
        layout_override=True           # direct implementation can work too
        @fy.layout(override=True)         # method layout decoration works too
        def layout(self):          
            return ft.Text("I am not a view")
            # returning one view means, forget everything, show me.
            return ft.View(controls=[ft.Text("I am a view")]) # try this instead

async def main(page):
    fy.fly(page)

    target_pages = ["home", "home/settings"]
    for _ in range(3):
        for p in target_pages:
            await asyncio.sleep(3)
            fy.fly(page, p)

ft.run(main)