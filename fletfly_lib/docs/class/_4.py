import asyncio
import flet as ft
import fletfly as fy

@fy.Route('{category}', layout_hero=False) # dynamic page
class Home:
    def layout(self, page):           # layout deleted once no view uses it(default)
        return ft.Column([
            ft.Text("Header"),
            fy.slot(page)
            ])
    view_hero = True                  # True means 5 in dynamic, 1 in static
    def view(self):
        return ft.Text("Main view")
    class User:
        path = ":id"                  # dynamic page
        @fy.Route.view(hero=2)           # max 2 pages are saved for different params
        def view(self, category, id):
            return ft.Column([
                    ft.Text(f" C: {category}"),
                    ft.Text(f"id: {id}")
                    ])

async def main(page):
    fy.fly(page)

    target_pages = ["a/1", "b/2", "c/3", 'd/4', 'e/5', 'f/6', 'g/7']
    for p in target_pages:
        await asyncio.sleep(2)
        fy.fly(page, p)

ft.run(main)