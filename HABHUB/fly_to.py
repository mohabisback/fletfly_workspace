import flet as ft
from fletfly import airway, Airline
import fletfly as fty

def main(page: ft.Page):
    # 1. تعريف المسار الجديد (المطار النهائي)
    new_route = airway(
        route="/new",
        land=lambda flyBox: ft.View(
            [ft.Text("Welcome to the New Airport! ✈️"), 
             ft.Button("Back to Home", on_click=lambda _: page.fly("/"))]
        )
    )

    # 2. تعريف المسار القديم (بوابة العبور)
    old_route = airway(
        route="/old",
        # المفروض الميدل وير ده ميتنفذش لو الـ fly_to اشتغلت
        fly_in=lambda flyBox: print("❌ Error: Middleware executed on a fly_to route!"),
        fly_to="/new" 
    )
    # 3. الصفحة الرئيسية للتجربة
    home_route = airway(
        route="/",
        land=lambda flyBox: ft.View(
            
            [
                ft.Text("Home Terminal 🏠"),
                ft.Button("Go to New (Direct)", on_click=lambda _: page.fly("/new")),
                ft.Text("Test the redirection:"),
                ft.Button("Go to Old (Should fly_to New)", on_click=lambda _: page.fly("/old")),
            ]
        )
    )

    # تجميع المطار (الـ Airline)
    # ملاحظة: تأكد من تمرير القائمة للمحرك بتاعك
    app_routes = [home_route, old_route, new_route]
    
    # هنا هتحط كود تشغيل الراوتر بتاعك (الـ flight_radar أو الـ engine)
    # مثال تخيلي حسب الكود اللي إنت شغال عليه:
    # router = FletFly(page, subways=app_routes)
    Airline(app_routes)
    fty.fly(page, '/new')
ft.run(main)