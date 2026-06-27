import asyncio
import flet as ft
import fletfly as fy

@fy.Route('blue', color='blue') 
@fy.Route('blue/red', color='red')  # Multi-decoration on the same class
class ColorPage:
    def view(self, color='black'): 
        return ft.Text(f"Color is {color}", color=color)

# Repetition by referencing the class directly
green = fy.Route(ColorPage, 'blue/red/green', color='green') 

# Repetition via copy (shallow copy of a route instance)
cyan = green.copy('blue/red/green/cyan', color='cyan')

async def main(page):
    fy.fly(page)
    target_pages = ['blue', 'blue/red', 'blue/red/green', 'blue/red/green/cyan']
    for p in target_pages:
        await asyncio.sleep(2)
        fy.fly(page, p)

ft.run(main)