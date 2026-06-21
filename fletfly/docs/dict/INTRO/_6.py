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

home = fy.Route({
    "path": None,                                  
    "layout": layout,
    "children": [
        {
            "path": "settings",                    # Sub route, path: "/home/settings"
            "layout": (settings_layout, {"override": True}), # with layout
            "layout_override": True                # in the route
        }
    ]
})

async def main(page):
    fy.fly(page)

    target_pages = ["home", "home/settings"]
    for _ in range(3):
        for p in target_pages:
            await asyncio.sleep(2)
            page.fly(p)

ft.run(main=main)