import flet as ft
import fletfly as fy
import asyncio
class A(fy.Route):      
    class B:
        class C:
            class D:
                class E:
                    @fy.child('red_page', color = 'red')   # add class as child
                    @fy.child(':color')                    # as dynamic child
                    class ColorPage:
                        def __init__(self, color='green'):
                            self.color = color
                        def view(self): return ft.Text(f"Color is {self.color}", color=self.color)
                    
                    page = fy.child(ColorPage, 'cyan_page',  color = 'cyan')   # child
                    green_page = fy.child(ColorPage, color = 'green')          # child
                    
                    children=[
                        fy.child('blue-page', ColorPage, color='blue'),        
                        fy.child(ColorPage, 'orange-page', color='orange')
                        ]
fy.Router(print_path_zone='/a/b/c/d/e', ) # print only this branch
async def main(page):
    fy.fly(page)
    target_pages = ['a/b/c/d/e/red-page', 'a/b/c/d/e/blue-page', 'a/b/c/d/e/orange-page',
                    'a/b/c/d/e/cyan', 'a/b/c/d/e/green-page', 'a/b/c/d/e/yellow']
    for _ in range(1): 
        for p in target_pages:
            await asyncio.sleep(2)
            page.fly(p)
ft.run(main)