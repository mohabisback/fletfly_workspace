import flet as ft
from fletfly import Route, Router, fly, child
import asyncio
class A(Route):      
    def view(self): return ft.Text('Normal class A view')
    class B:
        path = ":id"
        def view(self, id, color): return ft.Text(f"{id} page, color is {color}")
        class Fallback: # special fallback for zone C
            path = "*"
            def view(self): return ft.Text('Fallback for B zone')
    @child(path="*") # use path = "*" for fallback
    class Fallback:
        def view(self): return ft.Text('Fallback for A zone')

Router(error_path='a/*')
async def main(page):
    fly(page)
    target_pages = ['a/123?color="red"', 'a/b/c/d/e/f/g/h/i/j/k/l', 'a/m/n/o/p/q/r/s', 'something']
    for _ in range(3):
        for p in target_pages:
            await asyncio.sleep(5)
            page.fly(p)
ft.run(main)