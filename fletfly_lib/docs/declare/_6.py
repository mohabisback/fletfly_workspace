import asyncio
import flet as ft
import fletfly as fy 

def layout(page):
    return ft.Column([
        ft.Text('Header'),
        fy.slot(page)
    ])

def settings_layout():          
    return ft.Text("I am not a view")  
    # returning one view means, forget everything, show me.
    return ft.View(controls=[ft.Text("I am a view")]) # try this instead

# Declarative tree composition
home = fy.Route(
    fy.use.layout(layout),
    children=[
        fy.Route('settings',
            fy.use.layout(settings_layout, override=True), # override = layout_override
            layout_override=True, # layout_override
        )
    ]
)

async def main(page):
    fy.fly(page)

    target_pages = ["home", "home/settings"]
    for _ in range(3):
        for p in target_pages:
            await asyncio.sleep(2)
            fy.fly(page, p)

ft.run(main)