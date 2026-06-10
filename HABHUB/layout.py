import flet as ft
import fletfly as fty

@fty.fly_around
def shared_card_deck(page):
    return ft.TextField("shared_card", border_color="red")
@fty.fly_around
def shared_card_deck1(page):
    return ft.Container(
        content=ft.Column([
            ft.Text("SHARED DECK OF CARDS", size=11, color="amber", weight="bold"),
            ft.TextField(label="Type here to test Shared State")
        ]),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        padding=15,
        border_radius=8,
        border=ft.Border.all(2, ft.Colors.AMBER_400)
    )

@fty.route
class H:
    """الطبقة الخارجية - الغلاف الكلي باستخدام نظام الـ Slots الجديد المؤمن بالـ page session"""
    is_root = True
    layout_override = True 

    @staticmethod
    def layout(page):
        part1 = ft.Container(
            content=ft.Column([
                ft.TextField("root layout"),
                ft.Text("SYSTEM ROOT SHELL - SLOT A", size=12, weight="bold", color="white54"),
                fty.slot(page),
                fty.slot(page, "shared_card_deck", None, True)
            ]),
            bgcolor="#0F0F0F",
            border=ft.Border.all(5, ft.Colors.BLUE_GREY_900),
            padding=15,
            expand=True,
            border_radius=10
        )
        
        part2 = ft.Container(
            content=ft.Column([
                ft.Text("SYSTEM ROOT SHELL - SLOT B (SHARED)", size=12, weight="bold", color="white54"),
                ft.TextField("root layout"),
                # سلوت مسمى ومؤمن بالـ session لحمل الـ Around
                fty.slot(page, "shared_slot"),
                
            ]),
            bgcolor="#0F0F0F",
            border=ft.Border.all(5, ft.Colors.BLUE_GREY_900),
            padding=15,
            expand=True,
            border_radius=10
        )
        
        return part1, part2, 

    class A:
        """الطبقة المتوسطة - فريم الأدمن الأول"""
        layout_key = "admin_frame"
        layout_override = False 
        
        @staticmethod
        def frame(page):
            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.icons.Icons.ADMIN_PANEL_SETTINGS, color="amber"),
                        ft.Text("ADMINISTRATOR INTERFACE A", color="amber", weight="bold"),
                        ft.TextField("admin layout A"),
                    ]),
                    fty.slot(page),
                ]),
                bgcolor="#1A1A1A",
                border=ft.Border.all(4, ft.Colors.AMBER_900),
                padding=15,
                border_radius=8,
                expand=True
            )

    class B:
        """الطبقة المتوسطة - فريم الأدمن الثاني"""
        layout_key = "admin_frame"
        layout_override = False 
        
        @staticmethod
        def view(page):
            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.icons.Icons.ADMIN_PANEL_SETTINGS, color="amber"),
                        ft.Text("ADMINISTRATOR INTERFACE B", color="amber", weight="bold"),
                        ft.TextField("admin layout B"),
                    ]),
                    fty.slot(page),
                    fty.slot(page, "shared_slot")
                ]),
                bgcolor="#1A1A1A",
                border=ft.Border.all(4, ft.Colors.AMBER_900),
                padding=15,
                border_radius=8,
                expand=True
            ), {"shared_slot":fty.fly_around("shared_card_deck")}

        class X:
            """الطبقة الداخلية - المحتوى الفعلي X"""
            @staticmethod
            def view(page):
                return {
                    "": ft.Container(
                        content=ft.Column([
                            ft.Button("Y", on_click=lambda e: fty.fly(page, "/h/b/y")),
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.Icons.PERSON, size=40, color="blue"),
                                title=ft.Text("Mohab - Lead Engineer (X)", size=20),
                                subtitle=ft.Text("Suez, Egypt | HabHub System Active")
                            ),
                            fty.slot(page, "shared_card_deck", None, True),
                            ft.Divider(height=1, color="white10"),
                            ft.TextField("XXXXXXXXXXXXXXXXXXXXXXXX")
                        ]),
                        bgcolor="#252525",
                        border=ft.Border.all(3, ft.Colors.BLUE_700),
                        padding=20,
                        border_radius=5
                    ) #,"shared_slot": fty.fly_around("shared_card_deck"
            }

        class Y:
            """الطبقة الداخلية - المحتوى الفعلي Y"""
            @staticmethod
            def view(page):
                return {
                    "": ft.Container(
                        content=ft.Column([
                             ft.Button("X", on_click=lambda e: fty.fly(page, "/h/b/x")),
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.Icons.PERSON, size=40, color="blue"),
                                title=ft.Text("Mohab - Lead Engineer (Y)", size=20),
                                subtitle=ft.Text("Suez, Egypt | HabHub System Active")
                                
                            ),
                            ft.Divider(height=1, color="white10"),
                            
                            fty.slot(page, "shared_card_deck", None, True),
                            ft.TextField("YYYYYYYYYYYYYYYYYYYY")
                        ]),
                        bgcolor="#252525",
                        border=ft.Border.all(3, ft.Colors.BLUE_700),
                        padding=20,
                        border_radius=5
                    )#, "shared_slot": fty.fly_around("shared_test")
                }


def belal_layout2(page):
    layout = ft.Container(
        content=ft.Column([
            ft.Text("SYSTEM ROOT SHELL (BILAL)", size=12, weight="bold", color="white54"),
            fty.slot(page),
            fty.slot(page)
        ]),
        bgcolor="#0F0F0F",
        border=ft.Border.all(5, ft.Colors.BLUE_GREY_900),
        padding=15,
        expand=True,
        border_radius=10
    )
    return layout

def belal_view(page):
    part1 = ft.Container(
            content=ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.icons.Icons.PERSON, size=40, color="blue"),
                    title=ft.Text("Mohab - Lead Engineer", size=20),
                    subtitle=ft.Text("Suez, Egypt | HabHub System Active")
                ),
                ft.Divider(height=1, color="white10"),
                fty.slot(page, "shared_card_deck", None, True),
                ft.TextField("This is Belal view.")
            ]),
            bgcolor="#252525",
            border=ft.Border.all(3, ft.Colors.BLUE_700),
            padding=20,
            border_radius=5
        )
    return part1 # fty.fly_around("shared_card_deck")
    

page_dict = {"path": 'Bilal', "view": belal_view, "layout": belal_layout2, 'hero_view':True}
fty.Router([page_dict, H])    

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.title = "HabHub Layout Nesting Test - Slot System Enabled"
    fty.fly(page, "/h/b/x")
    #fty.fly(page, page.route if page.route else "/")

ft.run(main=main)