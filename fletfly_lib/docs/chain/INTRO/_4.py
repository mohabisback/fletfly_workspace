import asyncio
import flet as ft
import fletfly as fy 

def layout(page):           
    return ft.Column([
        ft.Text("Header"),
        fy.slot(page)
    ])

def view():
    return ft.Text("Main view")

def user_view(page):
    category = fy.fly(page).params.get("category", "default")
    user_id = fy.fly(page).params.get("id", "default")
    return ft.Column([
        ft.Text(f" C: {category}"),
        ft.Text(f"id: {user_id}")
    ])
# you can use layout_hero in root level, or hero in layout level
home = fy.Route("{category}", layout_hero=False).layout(layout).view(view, hero=True)
# True means 5 in dynamic, 1 in static

home.child(":id").view(user_view, hero=2) # max 2 pages are saved for different params

async def main(page):
    fy.fly(page)

    target_pages = ["a/1", "a/2", "b/3", 'b/4', 'c/5', 'd/6']
    for p in target_pages:
        await asyncio.sleep(2)
        fy.fly(page, p)

ft.run(main)