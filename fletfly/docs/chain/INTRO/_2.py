
import fletfly as fy Router, Route, slot, fly, data, StackMode, Shared
import flet as ft
import asyncio # just for mocking time delay

class CardDeck(ft.TextField): pass
shared = Shared(CardDeck, value='same obj same data') # auto-named to CardDeck
CardDeck2 = Shared(CardDeck, value='its me everywhere')

home = Route()                  # Route detection: path auto named to "/home"

@home.use.layout
def layout(page):    # Auto-detected layout by names (layout, frame)
    return ft.Column([
        ft.Text("Header"),
        data(page, ft.Text("loading..."), value="names.0"), # for loader
        slot(page),        # Anonymous slot (auto-injected)
        slot(page, "slot_a"),   # named slot (auto-injected)
        slot(page),        # Anonymous slot (auto-injected)
        slot(page, "CardDeck2", shared=True) # stuck always
    ])

@home.use.loader
async def loader():          # auto detected lazy loader, injects data
    await asyncio.sleep(5)       # mocking delay for data fetching
    return {"names":["John"]}  # called by "names.0"

@home.use.view # Auto-detected index
def view():        # Auto-detected view by names:
    return (           # (build, content, component, element)
    {"slot_a": ft.Text("Sir")},   # Binds to slot named 'slot_a'
    ft.Text("Hi"),     # Binds to first available nameless slot
    "CardDeck"       # shared view returned as part of view
    )

user = Route(':id')        # Sub route detection, path: "/home/:id"

@user.use.view
def user_view(page):  # Injected into self or inheritable layout
    return (
        ft.Text(f"{page.fly.params.get('id','default')}"),   # URL params
        {"slot_a":ft.Text(f"{page.fly.query.get('color', 'default')}")}, # URL query
        "CardDeck"   # shared view returned as part of view
    )

@user.use.fly_in(inheritable = True, param1='a') # detected by decoration
# classmethod descriptor auto-unwrapped internally
def func(param1):
    return True

home.children.append(user)

# handed father of class (or list of fathers of classes)
Router(home, initial_route = "/home", error_path="/home", every_level_fallback=False, max_views=5, 
       stack_mode=StackMode.root_all_from_last_home, detect_route_subclasses=False, print_debugs=True)


async def main(page):
    fly(page)

    target_pages = ["home/123", "home/456", "home/999", 'home/100']
    for p in target_pages:
        await asyncio.sleep(10)
        page.fly(p)

ft.run(main)