import asyncio # just for mocking time delay
import flet as ft
import fletfly as fy

class CardDeck(ft.TextField): pass

# Auto-detected & named 'CardDeck'
fy.Shared(CardDeck, value='same obj same data') 

# Explicitly named and registered via Router
CardDeck2 = fy.Shared('CardDeck2', CardDeck, value='its me everywhere')

def layout(page):    
    return ft.Column([
        ft.Text("Header"),
        fy.data(page, ft.Text("loading..."), value="names.0"), # for loader
        fy.slot(page),              # Anonymous slot (auto-injected)
        fy.slot(page, "slot_a"),    # named slot (auto-injected)
        fy.slot(page),              # Anonymous slot (auto-injected)
        fy.slot(page, "CardDeck2", shared=True) # stuck always
    ])

async def loader():          
    await asyncio.sleep(4)      # mocking delay for data fetching
    return {"names":["John"]}   # called by "names.0"

def view():
    return (           
    {"slot_a": ft.Text("Sir")},   # Binds to slot named 'slot_a'
    ft.Text("Hi"),      # Binds to first available nameless slot
    "CardDeck"          # shared view returned as part of view
    )

def user_view(page):  # Injected into self or inheritable layout
    return (
        ft.Text(f"{fy.fly(page).params.get('id','default')}"),   # URL params
        {"slot_a":ft.Text(f"{fy.fly(page).query.get('color', 'default')}")}, # URL query
        "CardDeck"   # shared view returned as part of view
    )

def func(param1):
    return True

home = fy.Route(
    fy.use.layout(layout), 
    fy.use.loader(loader), 
    fy.use.view(view),
    children=[
        fy.Route(':id', # Sub route, path: "/home/:id"
            fy.use.view(user_view), 
            fy.use.fly_in(func, inheritable=True, param1='a') 
        )
    ]
)

fy.Router(routes=[home], shared=[CardDeck2], initial_route = "/home",
          error_path="/home", every_level_fallback=False, max_views=5, 
       stack_mode=fy.StackMode.root_all_from_last_home, print_debugs=True)

async def main(page):
    fy.fly(page)

    target_pages = ["home/123", "home/456", "home/999", 'home/100']
    for p in target_pages:
        await asyncio.sleep(5)
        fy.fly(page, p)

ft.run(main)