import asyncio
import flet as ft
import fletfly as fy

def color_page(color='green'): 
    return ft.Text(f"Color is {color}", color=color)

# Auto detected route and injected beside its brothers in the tree
fy.Route('a/b/c/d/e/blue').view(color_page).props(color='blue')

# handed to Router, also injected in the tree beside its brothers
green_page = fy.Route('a/b/c/d/e/green').view(color_page).props(color='green')

a = fy.Route('a')\
    .layout(lambda page: (ft.Text("Layout Header"), fy.slot(page)))\
    .fly_in(lambda: True)  # middleware for all descendents))
e = a.child('b').child('c').child('d').child('e')

e.child('red').view(color_page).props(color='red')
e.child(':color').view(color_page)

fy.Router([a, green_page], print_path_zone='/a/b/c/d/e') # print only this branch

async def main(page):
    fy.fly(page)
    target_pages = [
        'a/b/c/d/e/red', 'a/b/c/d/e/blue', 'a/b/c/d/e/orange',
        'a/b/c/d/e/cyan', 'a/b/c/d/e/green', 'a/b/c/d/e/yellow'
    ]
    for _ in range(1): 
        for p in target_pages:
            await asyncio.sleep(2)
            fy.fly(page, p)

ft.run(main)