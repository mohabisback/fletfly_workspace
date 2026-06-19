import flet as ft
import fletfly as fy Route, Router, fly, child
import asyncio

a = Route()
b = Route()
c = Route()
d = Route()
e = Route()

# Hierarchy assembly
a.children.append(b)
b.children.append(c)
c.children.append(d)
d.children.append(e)

cyan_page = Route(color='cyan')

@cyan_page.use.view                      # add function as view
@e.use.child('red_page', color='red')    # add function as child
@e.use.child(':color')                   # as dynamic child
def color_page(color='green'): 
    return ft.Text(f"Color is {color}", color=color)
e.use.child('green_page', color='green')(color_page) # as child

e.children.extend([
            cyan_page,
            child('blue-page' ,color_page, color='blue'),
            child(color_page, 'orange-page', color='orange')
])

Router(a, print_path_zone='/a/b/c/d/e') # print only this branch

async def main(page):
    fly(page)
    target_pages = [
        'a/b/c/d/e/red-page', 'a/b/c/d/e/blue-page', 'a/b/c/d/e/orange-page',
        'a/b/c/d/e/cyan', 'a/b/c/d/e/green-page', 'a/b/c/d/e/yellow'
    ]
    for _ in range(1): 
        for p in target_pages:
            await asyncio.sleep(3)
            page.fly(p)

ft.run(main)