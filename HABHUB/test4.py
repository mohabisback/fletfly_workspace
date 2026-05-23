import flet as ft
import asyncio

async def main(page: ft.Page):
    page.title = "ألف باء برمجة - اختبار الحبس"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # ده الـ Layout اللي هيظهر ويختفي
    # خليناه Container بسيط جواه Column
    confirm_layout = ft.Container(
        content=ft.Column([
            ft.Text("تأكيد العملية", size=25, weight="bold"),
            ft.Row([
                ft.ElevatedButton("موافق (True)", on_click=lambda _: set_result(True), bgcolor="green", color="white"),
                ft.ElevatedButton("إلغاء (False)", on_click=lambda _: set_result(False), bgcolor="red", color="white"),
            ], alignment="center")
        ], alignment="center", horizontal_alignment="center"),
        bgcolor=ft.Colors.YELLOW_100,
        border=ft.border.all(2, ft.Colors.BLACK),
        border_radius=15,
        width=300,
        height=200,
        visible=False # مخفي في البداية
    )

    # الحدث اللي هيفرمل الكود
    confirm_event = asyncio.Event()
    final_choice = [None]

    def set_result(choice):
        final_choice[0] = choice
        confirm_layout.visible = False # إخفاء الـ Layout
        page.update()
        confirm_event.set() # فك الحبس

    async def start_process(e):
        print("1. الزرار اتداس.. بنظهر الـ Layout ونحبس الكود")
        confirm_layout.visible = True
        page.update()
        
        # الفرامل اليدوية
        await confirm_event.wait()
        
        # الكود مش هيوصل هنا غير لما تدوس على زرار من الـ Layout
        print(f"2. النتيجة هي: {final_choice[0]}")
        page.add(ft.Text(f"تمت العملية بقرار: {final_choice[0]}", size=20, color="blue"))
        page.update()
        
        # إعادة تهيئة للمرة الجاية
        confirm_event.clear()

    # بناء الصفحة
    page.add(
        ft.Stack([
            # الطبقة الأساسية
            ft.Column([
                ft.ElevatedButton("شغل الحارس واستنى النتيجة", on_click=start_process),
            ], alignment="center", horizontal_alignment="center", expand=True),
            
            # طبقة الحارس (الـ Layout)
            ft.Row([confirm_layout], alignment="center", vertical_alignment="center", expand=True)
        ], expand=True)
    )

ft.run(main)