import flet as ft
import fletfly as fy 
import _11a as Project1 # import module of sub project

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
        fy.Zone(
            modules= Project1,      # you have to pass the module itself
            routes = Project1.home, # we can't auto-detect unless wrapped
          # shared = Project1.shared   # it is auto-detected by wrapping
            path = 'project',    
            )       
    ]
}

fy.Router(home)

async def main(page):
    fy.fly(page)

ft.run(main=main)