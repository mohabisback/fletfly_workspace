import asyncio
import flet as ft
import fletfly as fy

def color_page(color='green'): 
    return ft.Text(f"Color is {color}", color=color)

# Auto detected, injected directly beside his deeply nested brothers
fy.Route('a/b/c/d/e/blue', color_page, color='blue') 
# Delivered directly to the router
green_page = fy.Route('a/b/c/d/e/green', fy.use.view(color_page, color='green'))

# Declarative tree composition
a = fy.Route('a',
    layout=lambda page: (ft.Text("Layout Header"), fy.slot(page)), 
    fly_in=lambda: True,  # middleware for all descendents)
    children=[
        fy.Route('b',
            children=[
                fy.Route('c',
                    children=[
                        fy.Route('d',
                            children=[
                                fy.Route('e',
                                    fy.use.child('red', fy.use.view(color_page, color='red')),
                                    children=[
                                        fy.Route(':color', fy.use.view(color_page))
                                            ],
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )

fy.Router([a, 'green_page'], print_path_zone='/a/b/c/d/e') # print only this branch

async def main(page):
    fy.fly(page)
    target_pages = [
        'a/b/c/d/e/red', 'a/b/c/d/e/blue', 'a/b/c/d/e/orange',
        'a/b/c/d/e/cyan', 'a/b/c/d/e/green', 'a/b/c/d/e/yellow'
    ]
    for _ in range(1): 
        for p in target_pages:
            await asyncio.sleep(2)
            page.fly(p)

ft.run(main)