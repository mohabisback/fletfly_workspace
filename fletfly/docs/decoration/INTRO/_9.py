import asyncio
import flet as ft
from fletfly import Router, Route, data, fly

home = Route()

@home.at.loader
async def loader():
    await asyncio.sleep(3)    # mocking data of 100 products
    return {"products":[         
            {"name": f"Product {i + 1}",
            "price": f"{ (i + 1) * 10 }$"}
            for i in range(100)]}

@home.at.view
def view(page): 
    return ft.GridView(expand=True, max_extent=200, spacing=10, controls =[
            ft.Card(content=ft.Column(alignment=ft.Alignment.CENTER, controls=[
                data(page, 
                    ft.Text(value='loading...',
                             size=16,
                             weight='bold'),
                    value=f"products.{i}.name"),
                data(page, 
                    ft.Text(value='loading...',
                             size=14,
                             color='green'),
                    value=f"products.{i}.price")
            ]))
            for i in range(100)
        ])   

ft.run(fly)