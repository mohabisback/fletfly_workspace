import asyncio
import flet as ft
import fletfly as fy

@fy.Route('dashboard', n='Dashboard', fly_to='settings') # overrides fly_to='home'
@fy.Route('error', n='Error', fly_to=None) # overrides fly_to='home'
@fy.Route('about', n='About') # fly_to will still be 'home' as the class
class General:
    fly_to = 'home'    # class level property, for redirecting all routes
    def view(self, n):
        return ft.Text(f"{n} Page")

class Settings(fy.Route):
    def view(self):
        return ft.Text("Settings Page")

class Home(fy.Route):
    def view(self):
        return ft.Text("Home Page")

async def main(page):
    fy.fly(page, 'home')

    targets = ['dashboard', 'error', 'about']
    for t in targets:
        await asyncio.sleep(3)
        fy.fly(page, t)

ft.run(main)