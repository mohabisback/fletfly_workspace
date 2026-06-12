# fletfly
**The Component Composition Engine for Flet.**

"Stop writing procedural routing logic. with `fletfly`, fly with flet."


## quick start

```python
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
```
---

## Medium start
Look at this single block of code. It demonstrates:
- auto detection of routes, nested subroutes.
- auto-path-naming (static & dynamic).
- hierarchical layout inheritance, and final views.
- multi & inheritable middlewares system.
- lazy loading data injection into already opened pages.
- named and nameless slots(outlets) injection.
- detection by decoration or inheritance and auto detection by names.
- all can be CBV instance dependent or static.
- index detection (for index using programmers).
- auto arguments manipulation, delivering what's needed including params & query.
- start router with different options.

```python
from fletfly import Router, Route, slot, fly, child, data, fly_in, NavigateStyle
import flet as ft
import asyncio # just for mocking time delay

def check_online():            # general middleware without params
    return True
def check_color(param1):       # general middleware with params
    if param1 == 'c': return True

class Home():             # Route detection: path auto named to "/home"
    def layout(self, page):    # Auto-detected layout by names (layout, frame)
        return ft.Column([
            ft.Text("Header"),
            slot(page),        # Anonymous slot (auto-injected)
            data(page, ft.Text("loading..."), value="names.0"), # for loader
            slot(page, "slot_a"),   # named slot (auto-injected)
        ])
    async def loader(self):          # auto detected lazy loader, injects data
        await asyncio.sleep(3)       # mocking delay for data fetching
        return {"names":["John"]}  # called by "names.0"
    class Index:               # Auto-detected index
        def view(self):        # Auto-detected view by names:
            return (           # (build, content, component, element)
            {"slot_a": ft.Text("Sir")},   # Binds to slot named a
            ft.Text("Hi")      # Binds to first available nameless slot
            )
    class _Helper: pass        # Private scope (ignored by router)

    @child(":id")              # Sub route detection, path: "/home/:id"
    class User:
        def view(self, page):  # Injected into self or inheritable layout
            return (
                ft.Text(f"{page.fly.params.get('id','default')}"),   # URL params
                {"slot_a":ft.Text(f"{page.fly.query.get('color', 'default')}")} # URL query
            )
        def fly_in_self(self, id, color='default'): # middleware, auto arguments detection
            if id == '123': return True # passage granted
            else: return '/home'        # redirect to '/home'
        
        @fly_in(inheritable = True, param1='a')
        @classmethod                    # classmethod descriptor auto-unwrapped internally
        def func(cls, param1):
            return True
        
        fly_in_c = check_online                                # static imported from outside
        fly_in_d = fly_in(check_color, param1='c', param2='b') # static imported from outside

# handed father of class (or list of fathers of classes)
Router(Home, initial_route = "/home", error_path="/home", every_level_fallback=False, max_views=5, 
       navigate_style=NavigateStyle.home_all_from_last_port, detect_route_subclasses=False, print_debugs=True)

def main(page):
    fly(page)
ft.run(main)    
```

**[Understand State Persistence & Overriding](docs/class/ATTRIBUTES.md)**


---
## Persistent Engine: Intelligent Reconciliation & Overriding
No matter how many views you are opening in the views stack, and how many navigations you made, you only use 1 instance of each layout, 1 instance of each view or shared view, and you can choose whether to garbage it at the end of its usage or keep it alive by the view_hero & layout_hero options.

```Python
class Home(Route):
    layout_hero = False                                # layout deleted once no view uses it(default)
    def layout(page):                                  # layout initialized once till no use
        return ft.Column([Header(), slot(page)])

    view_hero = True                                   # view persistant for re-use (True for static path)
    def view(page):
        return AnalyticsDashboard()
    class User:
        path = ":id"                                   # dynamic page
        layout_override = True                         # parent layouts cleared

        view_hero = 10                                 # max 10 pages are saved for different params (default = 5)
        def view(page):
            return ft.View(ft.Text("Complete page"))   # no layout, direct page injection
```

**[Understand State Persistence & Overriding](docs/class/LAYOUT.md)**

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