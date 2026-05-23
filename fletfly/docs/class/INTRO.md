# fletfly
**The Component Composition Engine for Flet.**

"Stop writing procedural routing logic. `fletfly` injects data into your builds, nests views and shared components into multi-layered layouts, reconciles the tree, and preserves state—all with built-in middlewares, microfrontend nav and zero boilerplate."

---

## The 20-Line Engine Shock
Look at this single block of code. It demonstrates auto-pathing (static & dynamic), dynamic (nameless) slot injection, and hierarchical layout inheritance—all without a single manual routing string or `page.add()` call.

```python
from fletfly import Airway, slot
import flet as ft

class Home(Airway):                          # Route detection: path auto named to "/home"
    def layout(page):                        # Auto-detected layout by names (layout, frame)
        return ft.Column([
            ft.Text("Header"),
            slot(page),                      # Anonymous slot (auto-injected)
            slot(page),                      # Anonymous slot (auto-injected)
            ft.Text("Footer")
        ])
        
    def build(page):                         # Auto-detected build by names (view, content, component, element)
        return (
            ft.Text("Hi"),                   # Binds to first available slot
            ft.Text("Welcome home")          # Binds to second available slot
        )
    
    class _Helper:                           # Private scope (ignored by router)
        pass

    @Airway(":id")                           # Sub route detection, path: "/home/:id"
    class User:
        def build(page):                     # Injected into self or inheritable layout
            return (
                ft.Text(f"{page.fly.params['id']}"),        # Accesses resolved URL params
                ft.Text(f"{page.fly.query['favourites']}")  # Accesses resolved URL query
            )
```
* **[Understand State Persistence & Overriding](docs/class/ATTRIBUTES.md)** *


---
## Persistent Engine: Intelligent Reconciliation & Overriding
No matter how many views you are opening in the views stack, and how many navigations you made, you only use 1 instance of each layout, 1 instance of each build or shared build, and you can choose whether to garbage it at the end of its usage or keep it alive by the build_hero & layout_hero options.

```Python
class Home(Airway):
    layout_hero = False                                # layout deleted once no view uses it(default)
    def layout(page):                                  # layout initialized once till no use
        return ft.Column([Header(), slot(page)])

    build_hero = True                                  # build persistant for re-use (True for static path)
    def build(page):
        return AnalyticsDashboard()
    class User:
        path = ":id"                                   # dynamic page
        layout_override = True                         # parent layouts cleared

        build_hero = 10                                # max 10 pages are saved for different params (default = 5)
        def build(page):
            return ft.View(ft.Text("Complete page"))   # no layout, direct page injection
```

* **[Understand State Persistence & Overriding](docs/class/LAYOUT.md)** *

---












2. Layout Overrides
Break the inheritance gracefully when you need an isolated view (like a login or settings page) within a nested structure.

```python
    @Airway("settings", layout_override=True)
    class Settings:
        def layout(page):
            # This layout acts as a new root, ignoring the parent's structure
            return ft.Row([slot(page)])

        def build(page):
            return ft.Text("Settings Panel")
```