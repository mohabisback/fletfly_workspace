import flet as ft
from fletfly import Route, slot, fly, fly_in

class Home(Route):             # Route detection: path auto named to "/home"
    def layout(self, page):    # Auto-detected layout
        return ft.Column([
                ft.Text("Header"),
                slot(page)     # Nameless slot for injection
            ])
    @classmethod
    def fly_in_1(cls):           # Middleware
        return True
    @staticmethod               
    def about():               # Sub method route detection, auto named to "/home/about"
        return ft.Text("about page")         # injected into self layout
    
    class User:                # Sub class route detection, auto named to "/home/user"
        @classmethod
        def view(cls):            # main view detection, injected into self or parent layout
            return ft.Text("User page")      # injected into parent layout
ft.run(fly)                  # Start Router, with auto detection of routes.