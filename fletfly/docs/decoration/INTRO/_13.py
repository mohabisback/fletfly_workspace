import flet as ft
import fletfly as fy 
import asyncio

a = fy.Route()
b = fy.Route()
c = fy.Route()
d = fy.Route()
e = fy.Route()

# Hierarchy assembly
a.children.append(b)
b.children.append(c)
c.children.append(d)
d.children.append(e)

cyan_page = fy.Route(color='cyan')

@cyan_page.use.view                      # add function as view
@e.use.child('red_page', color='red')    # add function as child
@e.use.child(':color')                   # as dynamic child
def color_page(color='green'): 
    return ft.Text(f"Color is {color}", color=color)
e.use.child('green_page', color='green')(color_page) # as child

e.children.extend([
            cyan_page,
            fy.child('blue-page' ,color_page, color='blue'),
            fy.child(color_page, 'orange-page', color='orange')
])

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