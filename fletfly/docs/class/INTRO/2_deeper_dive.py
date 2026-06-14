# docs/class/INTRO/deeper_dive.py
from fletfly import Router, Route, slot, fly, child, data, fly_in, NavigationStyle, Shared
import flet as ft
import asyncio # just for mocking time delay

@Shared('CardDeck2', value='its me everywhere')
@Shared(value='same obj same data') # auto named to 'CardDeck'
class CardDeck(ft.TextField): pass

class Home():                  # Route detection: path auto named to "/home"
    
    def layout(self, page):    # Auto-detected layout by names (layout, frame)
        return ft.Column([
            ft.Text("Header"),
            data(page, ft.Text("loading..."), value="names.0"), # for loader
            slot(page),        # Anonymous slot (auto-injected)
            slot(page, "slot_a"),   # named slot (auto-injected)
            slot(page),        # Anonymous slot (auto-injected)
            slot(page, "CardDeck2", shared=True) # sticked always
        ])
    
    async def loader(self):          # auto detected lazy loader, injects data
        await asyncio.sleep(5)       # mocking delay for data fetching
        return {"names":["John"]}  # called by "names.0"
    
    class Index:               # Auto-detected index
    
        def view(self):        # Auto-detected view by names:
            return (           # (build, content, component, element)
            {"slot_a": ft.Text("Sir")},   # Binds to slot named 'slot_a'
            ft.Text("Hi"),     # Binds to first available nameless slot
            "CardDeck"       # shared view returned as part of view
            )
    
    class _Helper: pass        # Private scope (ignored by router)

    @child(":id")              # Sub route detection, path: "/home/:id"
    class User:
    
        def view(self, page):  # Injected into self or inheritable layout
            return (
                ft.Text(f"{page.fly.params.get('id','default')}"),   # URL params
                {"slot_a":ft.Text(f"{page.fly.query.get('color', 'default')}")}, # URL query
                "CardDeck"   # shared view returned as part of view
            )
    
        @fly_in(inheritable = True, param1='a') # detected by decoration
        @classmethod             # classmethod descriptor auto-unwrapped internally
        def func(cls, param1):
            return True

# handed father of class (or list of fathers of classes)
Router(Home, initial_route = "/home", error_path="/home", every_level_fallback=False, max_views=5, 
       navigation_style=NavigationStyle.home_all_from_last_port, detect_route_subclasses=False, print_debugs=True)


async def main(page):
    fly(page)

    target_pages = ["home/123", "home/456", "home/999", 'home/100']
    for p in target_pages:
        await asyncio.sleep(10)
        page.fly(p)

ft.run(main)