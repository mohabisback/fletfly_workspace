import asyncio
import flet as ft
import fletfly as fy

def color_page(color='green'): 
    return ft.Text(f"Color is {color}", color=color)

blue_page = fy.Route(color_page, color='blue')
orange_page = fy.Route(fy.use.view(color_page), color='orange')

# Declarative tree composition
a = fy.Route('a',
    children=[
        fy.Route('b',
            children=[
                fy.Route('c',
                    children=[
                        fy.Route('d',
                            children=[
                                fy.Route('e',
                                    fy.use.child('green_page', fy.use.view(color_page, color='green')),
                                    fy.Route('cyan', fy.use.view(color_page), color='cyan'),
                                    blue_page,
                                    children=[
                                        fy.Route('red_page', fy.use.view(color_page), color='red'),   
                                        fy.Route(':color', fy.use.view(color_page)),                  
                                        orange_page
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

fy.Router(a, print_path_zone='/a/b/c/d/e') # print only this branch

async def main(page):
    fy.fly(page)
    target_pages = [
        'a/b/c/d/e/red-page', 'a/b/c/d/e/blue-page', 'a/b/c/d/e/orange-page',
        'a/b/c/d/e/cyan', 'a/b/c/d/e/green-page', 'a/b/c/d/e/yellow'
    ]
    for _ in range(1): 
        for p in target_pages:
            await asyncio.sleep(2)
            page.fly(p)

ft.run(main)