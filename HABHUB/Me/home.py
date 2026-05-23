import flet as ft

def get_view(page):

    def open_resizer(e):
        page.fly("/resizer")

    # قائمة الموديولات (عشان لو حبيت تضيف موديولات تانية بسهولة)
    modules = [
        {
            "title": "Image Resizer",
            "icon": ft.Icons.IMAGE_ASPECT_RATIO,
            "route": "/resize",
            "desc": "تغيير حجم الصور بدقة هندسية",
            "color": ft.Colors.BLUE_ACCENT
        },
        # {
        #     "title": "File Converter",
        #     "icon": ft.Icons.CHANGE_CIRCLE,
        #     "route": "/convert",
        #     "desc": "تحويل الملفات بين الصيغ المختلفة",
        #     "color": ft.Colors.ORANGE_ACCENT
        # },
    ]

    # بناء الكروت بتاعة الموديولات
    module_cards = []
    for mod in modules:
        module_cards.append(
            ft.Container(
                content=ft.Column([
                    ft.Icon(mod["icon"], size=40, color=mod["color"]),
                    ft.Text(mod["title"], weight=ft.FontWeight.BOLD),
                    ft.Text(mod["desc"], size=12, text_align=ft.TextAlign.CENTER, color=ft.Colors.GREY_400),
                    ft.Button("افتح الموديول", on_click=open_resizer)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=180,
                height=200,
                bgcolor=ft.Colors.ON_SURFACE_VARIANT,
                border_radius=15,
                padding=15,
                ink=True
            )
        )

    view = ft.View(
        appbar=ft.AppBar(
            title=ft.Text("HabHub Dashboard", weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor=ft.Colors.BLUE_GREY_900,
            color=ft.Colors.WHITE,
            actions=[ft.IconButton(ft.Icons.SETTINGS, icon_color=ft.Colors.WHITE)]
        ),
        controls=[
            ft.Column([
                ft.Container(height=20),
                ft.Text("مرحباً بك في منظومة HabHub", size=28, weight=ft.FontWeight.W_800),
                ft.Text("اختر الموديول الذي تود العمل عليه", size=16, color=ft.Colors.GREY_500),
                ft.Container(height=20),
                
                # عرض الموديولات في شكل Grid مرن
                ft.Row(
                    module_cards,
                    wrap=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.ADAPTIVE)
        ]
    )
    
    return view