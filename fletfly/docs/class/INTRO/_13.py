import flet as ft
import fletfly as fy
import asyncio

@fy.Route('a/b/c/d/e/blue', color = 'blue')   # add class as child
class ColorPage:
    path = ':color'
    def __init__(self, color='green'):
        self.color = color
    def view(self): return ft.Text(f"Color is {self.color}", color=self.color)

green_page = fy.Route(ColorPage, 'a/b/c/d/e/green',  color = 'green')          # child

class A(fy.Route):
    layout=lambda page: (ft.Text("Layout Header"), fy.slot(page))
    fly_in=lambda: True,  # middleware for all descendents)
    class B:
        class C:
            class D:
                class E:    
                    children=[
                        ColorPage       
                        ]
                    index = fy.child(ColorPage, 'cyan', color='cyan')                    
                    page = fy.child(ColorPage, 'red', color='red')

fy.Router([A, green_page], print_path_zone='/a/b/c/d/e', ) # print only this branch
async def main(page):
    fy.fly(page)
    target_pages = ['a/b/c/d/e/red', 'a/b/c/d/e/blue', 'a/b/c/d/e/orange',
                    'a/b/c/d/e/cyan', 'a/b/c/d/e/green', 'a/b/c/d/e/yellow']
    for _ in range(1): 
        for p in target_pages:
            await asyncio.sleep(2)
            page.fly(p)
ft.run(main)