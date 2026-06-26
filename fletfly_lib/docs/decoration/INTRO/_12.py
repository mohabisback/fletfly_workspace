import asyncio
import flet as ft
import fletfly as fy

a = fy.Route()  # Route detection: path auto named to "/a"

@a.use.view
def a_view(): 
    return ft.Text('Normal class A view')

a_fallback = fy.Route('*')

@a_fallback.use.view
def a_fallback_view(): 
    return ft.Text('Fallback for A zone')

b = fy.Route()

b_fallback = fy.Route('*')

@b_fallback.use.view
def b_fallback_view(): 
    return ft.Text('Fallback for B zone')

c = fy.Route(':id')

@c.use.view
def b_view(id, color): 
    return ft.Text(f"{id} page, color is {color}")

b.children.extend([c, b_fallback])
a.children.extend([b, a_fallback])

fy.Router(a, error_path='a/*')

async def main(page):
    fy.fly(page)
    target_pages = ['a/b/123?color="red"', 'a/b/c/d/e/f/g/h/i/j/k/l', 'a/m/n/o/p/q/r/s', 'something']
    for _ in range(3):
        for p in target_pages:
            await asyncio.sleep(2)
            fy.fly(page, p)

ft.run(main)