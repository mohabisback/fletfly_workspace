#ImageResizer.main.py
import flet as ft
import fletfly as fty
from fletfly import Airline, airway
from HABHUB.ImageResizer.home import get_view as get_home
from HABHUB.ImageResizer.about import get_view as get_about
from HABHUB.ImageResizer.error import get_view as get_err


# صفحة بسيطة
def test_view(page: ft.Page):
    return ft.View(
        controls=[
            ft.AppBar(title=ft.Text(f"Test View")),
            ft.Text("Welcome to FletFly 0.5!", size=30),
            ft.Button("Go to User 123", on_click=lambda _: page.fly("contact/test/user/123")),
            ft.Button("Search for 'Python'", on_click=lambda _: page.fly("contact/test/user/search?q=python&sort=newest")),
        ], 
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

# صفحة بـ Params (:id)
def profile_view(page: ft.Page):
    user_id = page.fly.params.get("id", "Unknown")
    return ft.View(
        controls=[
            ft.AppBar(title=ft.Text(f"Profile: {user_id}")),
            ft.Text(f"Viewing details for User ID: {user_id}", size=20, color="blue"),
            ft.Text(f"Page Instance: {hash(page)}", size=20, color="blue"),
            
            ft.Button("Back to Home", on_click=lambda _: page.fly("/")),
            ft.Button("Check another user (456)", on_click=lambda _: page.fly("contact/test/user/456")),
        ],
    )

# صفحة بـ Query Params (?q=...)
def search_view(page: ft.Page):
    query_text = page.fly.query.get("q")
    sort_by = page.fly.query.get("sort")
    return ft.View(
        controls=[
            ft.AppBar(title=ft.Text("Search Results")),
            ft.Text(f"Searching for: {query_text}", size=20, weight="bold"),
            ft.Text(f"Sorted by: {sort_by}"),
            ft.Button("Back to Home", on_click=lambda _: page.fly("/")),
        ],
    )




TITLE = "Hab Image Resizer"
Pages = {
        "":get_home,
        "error":get_err,
        "about":get_about,
        "contact":{
            "":get_about, #temp
            "email":test_view, #temp
            "phone":get_err, #temp
            "test":{
                "":test_view,
                "user":{
                    ":id":profile_view,
                    "search":search_view
                }
                }
            }
        }
airway = airway("", get_home,[
    airway("error", get_err),
    airway("about", get_about),
    airway("contact", get_about, [
        airway("email", test_view),
        airway("phone", get_err),
        airway("test", test_view, [
               airway("user", None, [
                   airway(":id", profile_view),
                   airway("search", search_view)
               ])
        ])
    ])
])

def main(page: ft.Page): # will never run in case of beeing sub project
    page.title = TITLE
    fty.Airline(page, airway, error_land="/error")

if __name__ == "__main__":
    ft.run(main)

