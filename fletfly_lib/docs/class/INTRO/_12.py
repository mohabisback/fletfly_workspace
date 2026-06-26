import asyncio
import flet as ft
import fletfly as fy
class A(fy.Route):      
    def view(self): return ft.Text('Normal class A view')
    class B:
        class C:
            path = ":id"
            def view(self, id, color): return ft.Text(f"{id} page, color is {color}")
        class Fallback: # special fallback for zone C
            path = "*"
            def view(self): return ft.Text('Fallback for B zone')
    @fy.child(path="*") # use path = "*" for fallback
    class Fallback:
        def view(self): return ft.Text('Fallback for A zone')

fy.Router(error_path='a/*')

async def main(page):
    fy.fly(page)
    target_pages = ['a/b/123?color="red"', 'a/b/c/d/e/f/g/h/i/j/k/l', 'a/m/n/o/p/q/r/s', 'something']
    for _ in range(1):
        for p in target_pages:
            await asyncio.sleep(2)
            fy.fly(page, p)
ft.run(main)