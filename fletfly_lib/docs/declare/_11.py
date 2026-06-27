import flet as ft
import fletfly as fy 
import _11a as Project1 # import module of sub project

class CardDeck(ft.TextField): pass
shared = fy.Shared(CardDeck, value='I am "CardDeck" shared of Main Zone')

def home_view(): 
    return (
        ft.Text("Main Home page"),
        ft.Button("Go Sub Project", on_click=lambda e: fy.fly(e.page, 'home/project')),
        'CardDeck' 
    )

project = fy.Zone(
    modules= Project1,          # module of second project
  # routes = Project1.home,     # if auto-detection is off
  # shared = Project1.shared,   # if auto-detection is off
  # path = 'project'            #if auto-naming is off
    )

home = fy.Route(
    fy.use.view(home_view),
    children=[
        project
    ]
)

ft.run(fy.fly)