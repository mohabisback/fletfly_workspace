
import flet as ft
import fletfly as fty
import asyncio
@fty.fly_decorator
async def confirm_exit_guard():
    # 1. بنخزن الصفحة في متغير محلي "ثابت" أول ما الدالة تبدأ
    page = fty.page 
    
    if page is None:
        print("ERROR: fty.page is None! Check if Airline initialized it.")
        return True

    confirm_event = asyncio.Event()
    user_choice = [False]

    # 2. دالة التعامل مع القرار
    def handle_click(choice):
        user_choice[0] = choice
        # هنا بقى بنستخدم 'page' المحلية اللي فوق، مش fty.page
        # الـ lambda هنا هتاخد الـ 'page' دي في حضنها (Closure)
        page.overlay.remove(guard_layout)
        page.update()
        confirm_event.set()

    # 3. بناء الـ Layout
    guard_layout = ft.Container(
        content=ft.Column([
            ft.Text("تنبيه يا هندسة!", size=20, weight="bold"),
            ft.Row([
                ft.ElevatedButton("أيوة، خرجني", on_click=lambda _: handle_click(True)),
                ft.ElevatedButton("لا، خليني", on_click=lambda _: handle_click(False)),
            ], alignment="center")
        ], tight=True, alignment="center"),
        bgcolor=ft.Colors.YELLOW_100,
        padding=20,
        border_radius=15,
        width=300,
    )

    # 4. التنفيذ
    page.overlay.append(guard_layout)
    page.update()

    # 5. الفرامل (الكلبشة)
    await confirm_event.wait()
    
    return user_choice[0]

def check_exit1():
    print("🚦 Attempt to exit!")
    return False # جرب تخليها False وشوف الزرار هيتحرك ولا لأ


# 1. صفحة القايمة الطويلة
def get_scroll_page(page: ft.Page):
    # بنعمل لستة طويلة جداً
    items = [ft.ListTile(title=ft.Text(f"Item Number {i}")) for i in range(100)]
    
    return ft.View( # حدد اسم الـ Argument صراحة
    controls=[            # وهنا الـ controls صراحة
        ft.AppBar(title=ft.Text("Scroll Test")),
        ft.TextField(),
        ft.Button("Go to Details", on_click=lambda _: page.fly("/t")),
        ft.ListView(controls=items, expand=True),
    ],
    on_confirm_pop=test_func
)
def test_func():
    print("Testing on_confirm_pop, it is good")
# 2. صفحة التفاصيل
def get_details_page(page: ft.Page):
    return ft.View(
        controls=[
            ft.AppBar(title=ft.Text("Details")),
            ft.Text("Now, click the back button or 'Fly Back'"),
            
            ft.TextField(),
            ft.Button("Fly Back to List", on_click=lambda _: page.fly("/t/tt")),
        ],
    on_confirm_pop=test_func
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
