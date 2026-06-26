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

# Chaining style composition
a = fy.Route().view(a_view)

# Branch 'b' and its children
b = a.child('b')
b.child(':id').view(b_view)
b.child('*').view(b_fallback_view)

# Fallback for 'a'
a.child('*').view(a_fallback_view)

fy.Router(error_path='a/*')

async def main(page):
    fy.fly(page)
    target_pages = ['a/b/123?color="red"', 'a/b/c/d/e/f/g/h/i/j/k/l', 'a/m/n/o/p/q/r/s', 'something']
    for _ in range(3):
        for p in target_pages:
            await asyncio.sleep(2)
            fy.fly(page, p)

ft.run(main)