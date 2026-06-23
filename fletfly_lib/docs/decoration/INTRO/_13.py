import flet as ft
import fletfly as fy 
import asyncio


# Auto detected by wrapping
blue_page=fy.Route(
    path="a/b/c/d/e/blue", # injected directly beside his brothers
    color="blue"
)

# delivered to router
green_page = fy.Route(
    path="a/b/c/d/e/green", # injected directly beside his brothers
)

a = fy.Route(
    path="a", 
    layout=lambda page: (ft.Text("Layout Header"), fy.slot(page)), 
    fly_in=lambda: True  # middleware for all descendents
)
b = fy.Route(path="b")
c = fy.Route(path="c")
d = fy.Route(path="d")
e = fy.Route(path="e")

a.children.append(b)
b.children.append(c)
c.children.append(d)
d.children.append(e)

@blue_page.use.view                 # route uses the func as view
@green_page.use.view(color='green') # route uses the func as view
@e.use.child('red', color='red')    # creates sub route with func as view
@e.use.child(':color')              # creates sub route with func as view
def color_page(color='black'): 
    return ft.Text(f"Color is {color}", color=color)

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
            page.fly(p)

ft.run(main=main)