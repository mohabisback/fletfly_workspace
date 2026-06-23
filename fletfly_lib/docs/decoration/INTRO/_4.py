import asyncio
import flet as ft
import fletfly as fy 

home = fy.Route("{category}", layout_hero=False) # layout_here in route

@home.use.layout
def layout(page):           
    return ft.Column([
        ft.Text("Header"),
        fy.slot(page)
    ])

@home.use.view(hero=True)         # True means 5 in dynamic, 1 in static
def view():
    return ft.Text("Main view")

user = fy.Route(":id")

@user.use.view(hero=2)            # max 2 pages are saved for different params
def user_view(page):
    category = page.fly.params.get("category", "default")
    user_id = page.fly.params.get("id", "default")
    return ft.Column([
        ft.Text(f" C: {category}"),
        ft.Text(f"id: {user_id}")
    ])

home.children.append(user)

async def main(page):
    fy.fly(page)

    target_pages = ["a/1", "a/2", "b/3", 'b/4', 'c/5', 'd/6']
    for p in target_pages:
        await asyncio.sleep(2)
        page.fly(p)

ft.run(main)