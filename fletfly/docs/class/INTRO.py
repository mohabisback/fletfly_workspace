from fletfly import Route, slot, fly, child
import flet as ft

class Home(Route):             # Route detection: path auto named to "/home"
    def layout(self, page):          # Auto-detected layout by names (layout, frame)
        return ft.Column([
            ft.Text("Header"),
            slot(page),        # Anonymous slot (auto-injected)
            slot(page),        # Anonymous slot (auto-injected)
            ft.Text("Footer")
        ])

    class Index:               # Auto-detected index
        def view(self):  # Auto-detected view by names:
            return (           # (build, content, component, element)
                ft.Text("Hi"), # Binds to first available slot
                ft.Text("Sir") # Binds to second available slot
            )
    
    class _Helper: pass        # Private scope (ignored by router)
 
    @child(":id")              # Sub route detection, path: "/home/:id"
    class User:
        def view(self, page):        # Injected into self or inheritable layout
            return (
                ft.Text(f"{page.fly.params['id']}"),        # URL params
                ft.Text(f"{page.fly.query['favourites']}")  # URL query
            )
ft.run(fly)                    # Start Router, with auto detecion of routes.