import asyncio
import flet as ft
import fletfly as fy

def a_view(): 
    return ft.Text('Normal class A view')

def a_fallback_view(): 
    return ft.Text('Fallback for A zone')

def b_fallback_view(): 
    return ft.Text('Fallback for B zone')

def b_view(id, color): 
    return ft.Text(f"{id} page, color is {color}")

# Declarative tree composition
a = fy.Route(  # Route detection: path auto named to "/a"
    fy.use.view(a_view),
    children=[
        fy.Route('b',
            children=[
                fy.Route(':id',
                    fy.use.view(b_view)
                ),
                fy.Route('*',
                    fy.use.view(b_fallback_view)
                )
            ]
        ),
        fy.Route('*',
            fy.use.view(a_fallback_view)
        )
    ]
)

fy.Router(a, error_path='a/*')

async def main(page):
    fy.fly(page)
    target_pages = ['a/b/123?color="red"', 'a/b/c/d/e/f/g/h/i/j/k/l', 'a/m/n/o/p/q/r/s', 'something']
    for _ in range(3):
        for p in target_pages:
            await asyncio.sleep(2)
            page.fly(p)

ft.run(main)