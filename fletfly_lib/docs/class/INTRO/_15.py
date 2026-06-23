"""
15. Redirecting With `fly_to` vs Directing with `fly`
### `fy.fly(page, route)`: 
- Initiates the core Router engine (if not initiated by `Router()` definition)
- Directing navigation on runtime for each user based on any conditions.
### `fly_to`
- Class/ Router level property, automatically intercepts and reroute traffic to another route.
"""
import asyncio
import flet as ft
import fletfly as fy
from fletfly import layout

@fy.Route('dashboard', n='Dashboard', fly_to='settings') # overrides fly_to='home'
@fy.Route('error', n='Error', fly_to=None) # overrides fly_to='home'
class Dashboard:
    fly_to = 'home'    # class level property, for redirecting all routes
    def view(self, n):
        return ft.Text(f"{n} Page")

class Settings(fy.Route):
    def view(self):
        return ft.Text("Settings Page")

async def main(page):
    # Determine the entry point dynamically per user condition
    if 1 == 1: 
        initial_page = 'dashboard'
    fy.fly(page, initial_page) # Initiate the router

    # force directing in a while
    await asyncio.sleep(5)
    page.fly('error')


ft.run(main=main)