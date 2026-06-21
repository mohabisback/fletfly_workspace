import flet as ft
import fletfly as fy 
from _11a import home as Project1 # Imported the Route instance instead of the class

shared = fy.Shared()
@shared.use.view(value='I am "CardDeck" shared of Main Zone')
class CardDeck(ft.TextField): pass

home = fy.Route() # Main project '/home'

@home.use.view
def home_view(): 
    return (
        ft.Text("Main Home page"),
        ft.Button("Go Sub Project", on_click=lambda e: e.page.fly('home/project')),
        'CardDeck' 
    )
    
project = fy.Zone(Project1) # Zone, auto named to '/home/project'
home.children.append(project)

ft.run(fy.fly)