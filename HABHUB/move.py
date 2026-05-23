import flet as ft

def main(page: ft.Page):
    page.title = "نقل عنصر واحد من مجموعة"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # الحاويات الرئيسية (المجموعات)
    source_column = ft.Column(spacing=10)
    target_column = ft.Column(spacing=10)

    # دالة النقل لعنصر واحد
    def move_single_item(e):
        # e.control هو الزر الذي تم الضغط عليه
        # e.control.data يحتوي على السطر (Row) بالكامل الذي نريد نقله
        target_row = e.control.data
        
        if target_row in source_column.controls:
            # 1. احذفه من المجموعة الأولى
            source_column.controls.remove(target_row)
            # 2. اقلب اتجاه السهم وشكله ليعود إذا ضغط عليه المستخدم مرة أخرى
            e.control.icon = ft.icons.Icons.ARROW_BACK
            e.control.tooltip = "إرجاع للمصدر"
            # 3. أضفه للمجموعة الثانية
            target_column.controls.append(target_row)
        else:
            # عملية عكسية للإرجاع
            target_column.controls.remove(target_row)
            e.control.icon = ft.icons.Icons.ARROW_FORWARD
            e.control.tooltip = "نقل للهدف"
            source_column.controls.append(target_row)

        # 4. تحديث المجموعات المصابة فقط ليعاد رسمها
        source_column.update()
        target_column.update()


    # إنشاء العناصر ديناميكياً ووضعها في المجموعة الأولى
    for i in range(1, 4):
        # سنضع الـ TextField والزر داخل Row ليكونوا وحدة واحدة
        item_row = ft.Row(vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        tf = ft.TextField(label=f"عنصر {i}", value=f"نص {i}", width=180)
        
        # الزر الذي سيقوم بنقل هذا الـ Row بالكامل
        btn = ft.IconButton(
            icon=ft.icons.Icons.ARROW_FORWARD,
            tooltip="نقل للهدف",
            on_click=move_single_item,
            # السر هنا: نربط كائن الـ Row بالزر عبر خاصية data لتسهيل استدعائه
            data=item_row 
        )
        
        # إضافة المكونات داخل الـ Row الموحد
        item_row.controls.extend([tf, btn])
        
        # إضافة الـ Row إلى المجموعة الأولى
        source_column.controls.append(item_row)


    # بناء تصميم الواجهة (تقسيم الشاشة لعمودين)
    page.add(
        ft.Row(
            controls=[
                # عمود المجموعة الأولى
                ft.Container(
                    content=ft.Column([
                        ft.Text("المجموعة الأولى (Source)", weight="bold", size=16),
                        source_column
                    ]),
                    bgcolor=ft.Colors.BLUE_GREY_50,
                    padding=15,
                    border_radius=10,
                    expand=True,
                    alignment=ft.alignment.Alignment.TOP_CENTER
                ),
                # فاصل صغير بين العمودين
                ft.VerticalDivider(width=10),
                # عمود المجموعة الثانية
                ft.Container(
                    content=ft.Column([
                        ft.Text("المجموعة الثانية (Target)", weight="bold", size=16),
                        target_column
                    ]),
                    bgcolor=ft.Colors.GREEN_50,
                    padding=15,
                    border_radius=10,
                    expand=True,
                    alignment=ft.alignment.Alignment.TOP_CENTER
                ),
            ],
            expand=True
        )
    )

ft.app(target=main)