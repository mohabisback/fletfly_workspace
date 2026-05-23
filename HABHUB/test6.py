import flet as ft
import asyncio

async def main(page: ft.Page):
    page.title = "The Ultimate View Dialog Fix"

    # 1. بنبني الديالوج "على بياض" ونجهزه
    confirm_event = asyncio.Event()
    result = [None]

    def handle_click(choice):
        result[0] = choice
        # بنقفل الديالوج من الفيو اللي شايله
        page.views[-1].dialog.open = False
        page.views[-1].update()
        confirm_event.set()

    # ده الديالوج اللي هيتحقن في الفيو
    my_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("تنبيه الفابريكا"),
        content=ft.Text("لو الديالوج ده ظهر، يبقى إحنا كسبنا!"),
        actions=[
            ft.ElevatedButton("True", on_click=lambda _: handle_click(True)),
            ft.ElevatedButton("False", on_click=lambda _: handle_click(False)),
        ],
    )

    async def open_guard(e):
        # 2. بنفتح الديالوج اللي أوريدي موجود جوه الفيو
        page.views[-1].dialog.open = True
        page.views[-1].update()
        
        print(">>> الكود وقف مستني ردك...")
        await confirm_event.wait()
        e.control.text = f"النتيجة: {result[0]}"
        page.update()
        confirm_event.clear()

    # 3. بناء الفيو وحقن الديالوج فيه "من الأول"
    main_view = ft.View(
        controls=[
            ft.AppBar(title=ft.Text("View Dialog Test")),
            ft.Container(
                content=ft.Button("افتح الديالوج المحبوس", on_click=open_guard)
            )
        ],
        dialog=my_dialog # الحقنة هنا يا هندسة
    )

    page.views.append(main_view)
    page.update()

ft.run(main)