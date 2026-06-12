import flet as ft
from fletfly import Route, slot, fly

class Home(Route):             # Route detection: path auto named to "/home"
    def layout(self, page):    # Auto-detected layout by names (layout, frame)
        return ft.Column([
                ft.Text("Header"),
                slot(page)
            ])
    
    @staticmethod               
    def about():               # Sub method route detection, auto named to "/home/about"
        return ft.Text("about page")         # injected into self layout
    
    class User:                # Sub class route detection, auto named to "/home/user"
    
        @classmethod
        def view(cls):            # main view detection, injected into self or parent layout
            return ft.Text("User page")      # injected into parent layout
    
        def settings(self):        # sub method route detection, auto named to "/home/user/settings"
            return ft.Text("Settings page")  # injected into grandparent layout

ft.run(fly)                  # Start Router, with auto detection of routes.