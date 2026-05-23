import flet as ft

class Airline:
    def __init__(self):
        # محاكاة للمابز بتاعتك
        self.static_map = {"/": "Home Page", "/about": "About Page"}

    def ticket(self, page: ft.Page):
        # تجهيز شنطة اليوزر
        page.on_route_change = self._handle_route_change
        page.on_view_pop = self._handle_view_pop
        
        # أول رحلة
        page.run_task(page.push_route, "/")

    def _handle_route_change(self, e):
        # الـ page هنا في e.page
        p = e.page
        print(f"\n🚀 Route Change Event!")
        print(f"📄 Page Session ID: {p.session_id}")
        print(f"🔗 Target Route: {p.route}")
        
        # منطق بناء الفيو
        content = self.static_map.get(p.route, "404")
        p.views.append(
            ft.View(
                route=p.route,
                controls=[
                    ft.AppBar(title=ft.Text(f"Flying to {p.route}")),
                    ft.Text(f"Welcome to {content}", size=30),
                    ft.ElevatedButton("Go to About", on_click=lambda _: p.go("/about")),
                    ft.ElevatedButton("Back to Home", on_click=lambda _: p.go("/")),
                ]
            )
        )
        p.update()

    def _handle_view_pop(self, e):
        # الـ page هنا برضه في e.page
        p = e.page
        print(f"\n⬅️ View Pop Event!")
        print(f"📄 Page Session ID: {p.session_id}")
        
        if len(p.views) > 1:
            p.views.pop()
            top_view = p.views[-1]
            p.go(top_view.route)
        p.update()

# --- التشغيل ---
router = Airline()

def main(page: ft.Page):
    router.ticket(page)

ft.run(main, view=ft.AppView.WEB_BROWSER)