import flet as ft
import fletfly as fy
import asyncio # just for mocking time delay

@fy.Shared(value="It's me everywhere") # detected & auto named to 'CardDeck'
class CardDeck(ft.TextField): pass
# Explicitly named and registered via Router
shared = fy.Shared('CardDeck2', CardDeck, value='same obj same data')

class Home():                  # Route detection: path auto named to "/home"
    
    def layout(self, page):    # Auto-detected layout by names (layout, frame)
        return ft.Column([
            ft.Text("Header"),
            fy.data(page, ft.Text("loading..."), value="names.0"), # for loader
            fy.slot(page),        # Anonymous slot (auto-injected)
            fy.slot(page, "slot_a"),   # named slot (auto-injected)
            fy.slot(page),        # Anonymous slot (auto-injected)
            fy.slot(page, "CardDeck2", shared=True) # stuck always
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

    @fy.child(":id")              # Sub route detection, path: "/home/:id"
    class User:
    
        def view(self, page):  # Injected into self or inheritable layout
            return (
                ft.Text(f"{page.fly.params.get('id','default')}"),   # URL params
                {"slot_a":ft.Text(f"{page.fly.query.get('color', 'default')}")}, # URL query
                "CardDeck"   # shared view returned as part of view
            )
    
        @fy.fly_in(inheritable = True, param1='a') # detected by decoration
        @classmethod             # classmethod descriptor auto-unwrapped internally
        def func(cls, param1):
            return True

# handed father of class (or list of fathers of classes)
fy.Router(routes=[Home], shared=[shared], initial_route = "/home",
        error_path="/home", every_level_fallback=False, max_views=5, 
        stack_mode=fy.StackMode.root_all_from_last_home, detect_route_subclasses=False, print_debugs=True)


async def main(page):
    fy.fly(page)

    target_pages = ["home/123", "home/456", "home/999", 'home/100']
    for p in target_pages:
        await asyncio.sleep(5)
        page.fly(p)

ft.run(main)