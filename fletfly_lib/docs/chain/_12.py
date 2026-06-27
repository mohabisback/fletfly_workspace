import asyncio
import flet as ft
import fletfly as fy

a = fy.Route().children(
    fy.Route("b").view(lambda:ft.Text("B view")),
    fy.Route().path("c").view(lambda:ft.Text("C view"))
)
child_d = a.child().path('d').view(lambda:ft.Text("D view"))
child_e = a.child('e').view(lambda: ft.Text("E view"))
index = a.index().view(lambda: ft.Text("Index view"))
index2 = a.index().view(lambda: ft.Text("Final Index view")) # overrides previous

async def main(page):
    fy.fly(page)
    target_pages = ['/a', '/a/b', '/a/c', '/a/d', '/a/e']
    for item in target_pages:
        await asyncio.sleep(2)
        fy.fly(page, item)

ft.run(main)