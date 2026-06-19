import asyncio
import flet as ft
import fletfly as fy Route, fly, slot

home = Route()

@home.use.layout
def layout(page):
    return ft.Column([
        ft.Text('Header'),
        slot(page)
    ])

settings = Route('settings', layout_override=True) # layout_override

@settings.use.layout(override = True) # override = layout_override
def settings_layout():          
    return ft.Text("I am not a view")  
    # returning one view means, forget everything, show me.
    return ft.View(controls=[ft.Text("I am a view")]) # try this instead

home.children.append(settings)

async def main(page):
    fly(page)

    target_pages = ["home", "home/settings"]
    for _ in range(3):
        for p in target_pages:
            await asyncio.sleep(3)
            page.fly(p)

ft.run(main)