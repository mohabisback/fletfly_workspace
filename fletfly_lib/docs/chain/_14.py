import asyncio
import flet as ft
import fletfly as fy

class Home(fy.Route):
    def view(self):
        return ft.Button('Go Settings', on_click=lambda e: fy.fly(e.page, 'settings'))

class Settings(fy.Route):
    def view(self):
        return ft.Text("Settings Page")

async def main(page):
    # Determine the entry point dynamically per user condition
    if 1 == 1: 
        initial_page = 'home'
    fy.fly(page, initial_page) # Initiate the router

    # force directing in a while
    await asyncio.sleep(5)
    fy.fly(page, 'home')

ft.run(main)