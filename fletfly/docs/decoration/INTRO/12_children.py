import flet as ft
from fletfly import Route, Router, fly, child
import asyncio
class A(Route):      
    class B:
        class C:
            class D:
                class E:
                    @child('red_page', color = 'red')
                    @child(':color')
                    class ColoredPage:
                        def __init__(self, color='green'):
                            self.color = color
                        def view(self): return ft.Text(f"Color is {self.color}", color=self.color)
                    magenta_page = child(ColoredPage, color = 'magenta')
                    green_page = child(ColoredPage, color = 'green')
                    children=[
                        child(ColoredPage, 'blue-page', color='blue'),
                        child(ColoredPage, 'orange-page', color='orange')
                        ]
Router(print_path_zone='/a/b/c/d/e', )
async def main(page):
    fly(page)
    target_pages = ['a/b/c/d/e/red-page', 'a/b/c/d/e/blue-page', 'a/b/c/d/e/orange-page',
                    'a/b/c/d/e/brown-page', 'a/b/c/d/e/green-page', 'a/b/c/d/e/yellow']
    for _ in range(1): 
        for p in target_pages:
            await asyncio.sleep(3)
            page.fly(p)
ft.run(main)