import flet as ft
import fletfly as fy 
import _11a as Project1 # import the second project

class CardDeck(ft.TextField): pass
shared = fy.Shared().view(CardDeck).props(value='I am "CardDeck" shared of Main Zone')

def home_view(): 
    return (
        ft.Text("Main Home page"),
        ft.Button("Go Sub Project", on_click=lambda e: e.page.fly('home/project')),
        'CardDeck' 
    )

project = fy.Zone(
    modules= Project1,          # module of second project
  # routes = Project1.home,     # if auto-detection is off
  # shared = Project1.shared,   # if auto-detection is off
  # path = 'project'            #if auto-naming is off
    )

home = fy.Route().view(home_view)
home.child(project)

ft.run(fy.fly)