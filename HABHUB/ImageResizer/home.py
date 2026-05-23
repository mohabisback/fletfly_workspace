#/ImageResizer/home.py
import flet as ft
import fletfly.fletfly as fty
def get_view(page):

    TITLE = "Hab Image Resizer Pro"
    view = ft.View()
    view.bgcolor = "#f0f2f5" 
    view.vertical_alignment = "start"
    view.horizontal_alignment = "center"
    view.padding = 30

    btn_about = ft.Button("Go to about page", on_click=lambda e: fty.fly(page, "about"))

    # 2. المكونات (TextFields) بتنسيق شيك
    width_input = ft.TextField(
        label="Width (px)", 
        width=150, 
        border_radius=10, 
        prefix_icon=ft.Icons.WIDGETS_SHARP
    )
    height_input = ft.TextField(
        label="Height (px)", 
        width=150, 
        border_radius=10, 
        prefix_icon=ft.Icons.HEIGHT
    )

    view.appbar = ft.AppBar(
        title=ft.Text(TITLE, weight="bold", color="white"),
        center_title=True,
        bgcolor="#2e7d32", # أخضر غامق شيك
        actions=[
            ft.IconButton(ft.Icons.SETTINGS_OUTLINED, icon_color="white")
        ]
    )

    image_preview = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.IMAGE_OUTLINED, size=50, color="#9e9e9e"),
            ft.Text("No Image Selected", color="#9e9e9e")
        ], alignment="center", horizontal_alignment="center"),
        width=400,
        height=250,
        border=ft.Border.all(2, "#e0e0e0"),
        border_radius=15,
        bgcolor="white",
        margin=ft.Margin.only(bottom=20)
    )

    main_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Upload & Resize", size=22, weight="bold"),
                ft.Divider(),
                image_preview, btn_about,
                ft.Row([width_input, height_input], alignment="center", spacing=20),
                ft.Divider(),
                ft.Row([
                    ft.Button(
                        "Select Image", 
                        icon=ft.Icons.UPLOAD_FILE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        height=50
                    ),
                    ft.Button(
                        "Download Result", 
                        icon=ft.Icons.DOWNLOAD,
                        bgcolor="#1565c0",
                        color="white",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        height=50
                    ),
                ], alignment="center", spacing=20)
            ], horizontal_alignment="center"),
            padding=25,
            width=500
        ),
        elevation=10
    )

    view.controls.clear()
    view.controls.append(main_card)
    return view
