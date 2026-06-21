
import asyncio # just for mocking time delay
import flet as ft
import fletfly as fy

shared = fy.Shared() # Auto-named to CardDeck
@shared.use.view(value='its me everywhere')
class CardDeck(ft.TextField): pass

# Explicitly named & registered via Router.
CardDeck2 = fy.Shared('CardDeck2', CardDeck, value='same obj same data') # Explicitly named

home = fy.Route()  # Route detection: path auto named to "/home"

@home.use.layout
def layout(page):    
    return ft.Column([
        ft.Text("Header"),
        fy.data(page, ft.Text("loading..."), value="names.0"), # for loader
        fy.slot(page),        # Anonymous slot (auto-injected)
        fy.slot(page, "slot_a"),   # named slot (auto-injected)
        fy.slot(page),        # Anonymous slot (auto-injected)
        fy.slot(page, "CardDeck2", shared=True) # stuck always
    ])

@home.use.loader
async def loader():
    await asyncio.sleep(5)   # mocking delay for data fetching
    return {"names":["John"]}  # called by "names.0"

@home.use.view
def view():
    return (
    {"slot_a": ft.Text("Sir")},   # Binds to slot named 'slot_a'
    ft.Text("Hi"),      # Binds to first available nameless slot
    "CardDeck"          # shared view returned as part of view
    )

user = fy.Route(':id')

@user.use.view
def user_view(page):  # Injected into self or inheritable layout
    return (
        ft.Text(f"{page.fly.params.get('id','default')}"),   # URL params
        {"slot_a":ft.Text(f"{page.fly.query.get('color', 'default')}")}, # URL query
        "CardDeck"   # shared view returned as part of view
    )

@user.use.fly_in(inheritable = True, param1='a')
def func(param1):
    return True

home.children.append(user)

fy.Router(routes=[home], shared=[shared], initial_route = "/home",
        error_path="/home", every_level_fallback=False, max_views=5, 
        stack_mode=fy.StackMode.root_all_from_last_home, print_debugs=True)

async def main(page):
    fy.fly(page)

    target_pages = ["home/123", "home/456", "home/999", 'home/100']
    for p in target_pages:
        await asyncio.sleep(5)
        page.fly(p)

ft.run(main)