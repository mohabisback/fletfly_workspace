#main.py
import flet as ft
import fletfly as fty
from Me.home import get_view as get_home
from Me.error import get_view as get_err
from ImageResizer_main import Pages as ImageResizer
from ImageResizer_main import airway as ImageResizerAirzone

TITLE = "HabHub Mohab's Portal"
Pages = {
        "":get_home,
        "resizer": fty.Airzone(ImageResizer), # get you a sub home page
        "error":get_err,
        "contact":{
            "":get_home, #temp
            "email":get_err, #temp
            "phone":get_err, #temp
                }
        }


def fly_in1(page):
    return True
def fly_in2(page):
    return False
def fly_in2(page):
    return False
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
    user_id = page.params.get("id", "Unknown")
    return ft.View(
        controls=[
            ft.AppBar(title=ft.Text(f"Profile: {user_id}")),
            ft.Text(f"Viewing details for User ID: {user_id}", size=20, color="blue"),
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


airzone = fty.airway(path="/", builder=get_home, fly_in=fly_in1, subways=[
    
    # simple airway(route) with path(string) and builder(callable returns a view)
    fty.airway(path="/error", builder=get_err),

    # airway with subways(subroutes)
    fty.airway(path="/about", fly_out=fly_in2, builder=search_view, subways=[
        fty.airway(path="/contact_details", builder=profile_view),
        fty.airway(path="/chat", fly_out=fly_in2, builder=test_view)
        ]),
   
    fty.Airzone(ImageResizerAirzone, "/resizer") 
    ]),

fty.Airline(airzone, error_path="error", max_pads = 5)

def main(page: ft.Page):
    
    page.title = TITLE
    fty.fly(page)
if __name__ == "__main__":
    ft.run(main)