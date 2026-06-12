# fletfly
**The Component Composition Engine for Flet.**

"Stop writing procedural routing logic. `fletfly` injects data into your views, nests views and shared components into multi-layered layouts, reconciles the tree, and preserves state—all with built-in middlewares, microfrontend nav and zero boilerplate."

---

## The 20-Line Engine Shock
Look at this single block of code. It demonstrates auto-pathing (static & dynamic), dynamic (nameless) slot injection, and hierarchical layout inheritance—all.

```python
from fletfly import Route, slot, fly
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
        def view(self, data):        # Auto-detected view by names:
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
```
```terminal


```
* **[Understand State Persistence & Overriding](docs/class/ATTRIBUTES.md)** *


---
## Persistent Engine: Intelligent Reconciliation & Overriding
No matter how many views you are opening in the views stack, and how many navigations you made, you only use 1 instance of each layout, 1 instance of each view or shared view, and you can choose whether to garbage it at the end of its usage or keep it alive by the view_hero & layout_hero options.

```Python
class Home(Route):
    layout_hero = False                                # layout deleted once no view uses it(default)
    def layout(page):                                  # layout initialized once till no use
        return ft.Column([Header(), slot(page)])

    view_hero = True                                  # view persistant for re-use (True for static path)
    def view(page):
        return AnalyticsDashboard()
    class User:
        path = ":id"                                   # dynamic page
        layout_override = True                         # parent layouts cleared

        view_hero = 10                                # max 10 pages are saved for different params (default = 5)
        def view(page):
            return ft.View(ft.Text("Complete page"))   # no layout, direct page injection
```

* **[Understand State Persistence & Overriding](docs/class/LAYOUT.md)** *

---












2. Layout Overrides
Break the inheritance gracefully when you need an isolated view (like a login or settings page) within a nested structure.

```python
    @Route("settings", layout_override=True)
    class Settings:
        def layout(page):
            # This layout acts as a new root, ignoring the parent's structure
            return ft.Row([slot(page)])

        def view(page):
            return ft.Text("Settings Panel")
```