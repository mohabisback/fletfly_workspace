import asyncio
import flet as ft
import fletfly as fy

def color_page(color='green'): 
    return ft.Text(f"Color is {color}", color=color)

blue_page = fy.Route().view(color_page).props(color='blue')
orange_page = fy.Route().view(color_page).props(color='orange')

# Chaining style composition
a = fy.Route('a')
e = a.child('b').child('c').child('d').child('e')

e.child('green_page').view(color_page).props(color='green')
e.child('cyan').view(color_page, color='cyan')
e.child(blue_page)
e.child('red_page').view(color_page).props(color='red')
e.child(':color').view(color_page)
e.child(orange_page)

fy.Router(print_path_zone='/a/b/c/d/e') # print only this branch

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