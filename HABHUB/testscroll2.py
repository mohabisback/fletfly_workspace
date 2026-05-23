
import flet as ft
import fletfly as fty
import asyncio

async def confirm_exit_guard(page):
    view = page.airport
    
    # مسكنا العيال (الزراير والديالوج)
    dialog = view.custom_dialog
    btn_yes = view.btn_yes
    btn_no = view.btn_no
    
    confirm_event = asyncio.Event()
    user_choice = [False]

    # المنطق اللي هنحقنه في الـ on_click
    def handle_click(choice):
        user_choice[0] = choice
        dialog.visible = False
        # بنصفر الـ on_click تاني عشان النظافة
        btn_yes.on_click = None
        btn_no.on_click = None
        view.update()
        confirm_event.set()

    # حقن الأوامر في الزراير "على الحامي"
    btn_yes.on_click = lambda _: handle_click(True)
    btn_no.on_click = lambda _: handle_click(False)

    # إظهار النافذة
    dialog.visible = True
    print("I got hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    view.update()

    # الفرامل
    await confirm_event.wait()
    
    return user_choice[0]

def check_exit1():
    print("🚦 Attempt to exit!")
    return False # جرب تخليها False وشوف الزرار هيتحرك ولا لأ

def get_scroll_page(page: ft.Page):
    # الطبقة الأولى: محتويات الفيو الأصلية (الكونتينر اللي واخد المشهد كله)
    view_content = ft.Container(
        expand=True,
        content=ft.Column([
            ft.AppBar(title=ft.Text("Scroll Test")),
            ft.Button("Back but not that back", on_click=lambda p: page.fly("/t")),
            ft.TextField(""),
            ft.ListView(controls=[ft.ListTile(title=ft.Text(f"Item {i}")) for i in range(100)], expand=True),
        ])
    )

    # الطبقة الثانية: الديالوج (مستخبي في الأول)
    # بنعمله Container واخد الشاشة كلها عشان الـ transparent surroundings
    # ده الكونتينر "الحارس" اللي هيتحط في الـ Stack فوق محتوى الصفحة
    btn_yes = ft.Button("أيوة، خرجني", bgcolor="red", color="white")
    btn_no = ft.OutlinedButton("لا، خليني")

    custom_dialog = ft.Card(
            elevation=10,
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color="amber", size=40),
                    ft.Text("تأكيد الخروج", size=20, weight="bold"),
                    ft.Text("يا هندسة فيه بيانات ما اتسيفتش، متأكد إنك عايز تخرج؟", text_align="center"),
                    ft.Divider(),
                    ft.Row([btn_yes, btn_no
                    ], alignment="center", spacing=20)
                ], tight=True, alignment="center", horizontal_alignment="center"),
                padding=30,
                width=400, # عرض الكارد عشان مياخدش الشاشة كلها
            ), visible = False
        )

    # الفيو هو الـ Top Most وبياخد الـ Stack جواه
    new_view = ft.View(
        controls=[
            ft.Stack([
                view_content, # الطبقة اللي تحت
                custom_dialog # الطبقة اللي فوق
            ], expand=True)
        ]
    )
    
    # بنخزن المرجع عشان الحارس يلاقيه
    new_view.custom_dialog = custom_dialog
    new_view.btn_yes = btn_yes
    new_view.btn_no = btn_no
    return new_view
# 2. صفحة التفاصيل
def get_details_page(page: ft.Page):
    return ft.View(
        controls=[
            ft.AppBar(title=ft.Text("Details")),
            ft.Text("Now, click the back button or 'Fly Back'"),
            
            ft.TextField(),
            ft.Button("Fly Back to List", on_click=lambda _: page.fly("/t/tt")),
        ]
    )

# ضيفهم في الـ Pages بتاعتك
Pages = {
    "": lambda p: ft.Text("Home"),
    "t":{
        "":get_details_page,
        "tt": fty.fly_out(confirm_exit_guard)(get_scroll_page)
        }
        }
def main(page):
    fty.Airline(page,Pages)
ft.run(main)
