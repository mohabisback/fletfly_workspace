import asyncio
import flet as ft
import fletfly as fy

home_route = fy.Route("home").view(
    lambda: ft.Button('Go Settings', on_click=lambda e: fy.fly(e.page, 'settings'))
)

settings_route = fy.Route("settings").view(
    lambda: ft.Text("Settings Page")
)

async def main(page):
    # Determine the entry point dynamically per user condition
    if 1 == 1: 
        initial_page = 'home'
    
    # Initiate the router with the defined routes
    fy.fly(page, initial_page) 

    # force directing in a while
    await asyncio.sleep(5)
    fy.fly(page, 'home')

ft.run(main)