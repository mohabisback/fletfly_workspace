import flet as ft
import fletfly as fy 
from _11a import home as Project1 # Imported the Route instance instead of the class

class CardDeck(ft.TextField): pass
shared = fy.Shared().view(CardDeck).props(value='I am "CardDeck" shared of Main Zone')

def home_view(): 
    return (
        ft.Text("Main Home page"),
        ft.Button("Go Sub Project", on_click=lambda e: e.page.fly('home/project')),
        'CardDeck' 
    )

project = fy.Zone(Project1) # Zone, auto named to '/home/project'

home = fy.Route().view(home_view)
home.child(project)

ft.run(fy.fly)