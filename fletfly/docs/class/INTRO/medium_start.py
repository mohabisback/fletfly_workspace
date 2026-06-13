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