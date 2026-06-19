#main.py
import flet as ft
import fletfly as fty
from Me.home import get_view as get_home
from Me.error import get_view as get_err
from ImageResizer_main import Pages as ImageResizer
from ImageResizer_main import route as ImageResizerZone

TITLE = "HabHub Mohab's Portal"
Pages = {
        "":get_home,
        "resizer": fty.Zone(ImageResizer), # get you a sub home page
        "error":get_err,
        "contact":{
            "":get_home, #temp
            "email":get_err, #temp
            "phone":get_err, #temp
                }
        }


def fly_in1(page, msg):

    return True
def fly_in2():
    return True
def fly_in3(page):
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


zone = fty.route(path="/", viewer=get_home, fly_ins=[
    fty.fly_in(fly_in1, msg="done once every view of home page", inheritable=False),
    fly_in2, # default, done once every inheriting sub
    fty.fly_in(fly_in1, msg="repeated every sub view", apply_per_view=False),
    ], children=[
    
        # simple route(route) with path(string) and viewer(callable returns a view)
        fty.route(path="/error", viewer=get_err),

        # route with children(subroutes)
        fty.route(path="/:id", fly_out=fly_in2, viewer=search_view, children=[
            fty.route(fly_to="something", children=[
                fty.route(fly_to="something2"),
                fty.route(path="/[chat]", fly_out=fly_in2, viewer=test_view, children=[
                    fty.route('hi', layout=test_view, children=[
                        fty.route("bye", view=test_view),
                        fty.route("", view=test_view)
                    ])
                ])
            ])
        ]),
    
        fty.Zone(ImageResizerZone, "/resizer") 
        ]),

fty.Router(zone, error_path="error", max_views = 3, stack_mode= "all_views", print_path_zone="/")



class Flyer:
    name = "fixed"
    def __init__(self, name):
        self.name = name
    @staticmethod
    def fly_to(destination):
        return f"{Flyer.name} is fly_ing to {destination}!"
    bare_func = fly_to.__func__ if isinstance(fly_to, (staticmethod, classmethod)) else fly_to
    
    bare_func._info = "at 10 am"

# 1. Create an instance
plane = Flyer("Boeing 747")

# 2. Get the bound method dynamically
a = getattr(plane, "fly_to")
# 3. Call it
result = a("Cairo")
def test_main(page:ft.Page):
    
    page.title = TITLE
    fty.fly(page)
if __name__ == "__main__":
    ft.run(test_main)

