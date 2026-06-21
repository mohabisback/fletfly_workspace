import flet as ft
import fletfly as fy 
from _11a import home as subhome # Imported the Route configuration dict/tree
import _11a

class CardDeck(ft.TextField): pass

fy.Shared({ # Auto detected, named and added
    "view": CardDeck,
    "value": 'I am "CardDeck" shared of Main Zone'
})

def home_view(): 
    return (
        ft.Text("Main Home page"),
        ft.Button("Go Sub Project", on_click=lambda e: e.page.fly('home/project')),
        'CardDeck' 
    )

home = {
    "path": "home",
    "view": home_view,
    "children": [
        fy.Zone([
            subhome,    # we can't detect module of dict
            _11a        # you have to pass the module itself
            ],          # for auto-detection of routes and shared
            'project'
            )
    ]
}

fy.Router(home)

async def main(page):
    fy.fly(page)

ft.run(main=main)