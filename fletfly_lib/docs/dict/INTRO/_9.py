import asyncio
import flet as ft
import fletfly as fy

async def loader():
    await asyncio.sleep(3)    # mocking data of 100 products
    return {"products":[         
            {"name": f"Product {i + 1}",
            "price": f"{ (i + 1) * 10 }$"}
            for i in range(100)]}

def view(page): 
    return ft.GridView(expand=True, max_extent=200, spacing=10, controls =[
            ft.Card(content=ft.Column(alignment=ft.Alignment.CENTER, controls=[
                fy.data(page, 
                    ft.Text(value='loading...',
                             size=16,
                             weight='bold'),
                    value=f"products.{i}.name"),
                fy.data(page, 
                    ft.Text(value='loading...',
                             size=14,
                             color='green'),
                    value=f"products.{i}.price")
            ]))
            for i in range(100)
        ])   

home = {
    "path": "home",
    "loader": loader,
    "view": view
}

fy.Router(home)

async def main(page):
    fy.fly(page)

ft.run(main=main)