import flet as ft
import fletfly as fy
import _11a as Project1 # import module of sub project

@fy.Shared(value = 'I am "CardDeck" shared of Main Zone')
class CardDeck(ft.TextField): pass

class Home(fy.Route): # Main project '/home'
    def view(self): return (
                ft.Text ("Main Home page"),
                ft.Button("Go Sub Project", on_click=lambda e: e.page.fly('home/project')),
                'CardDeck' )
    
    project = fy.Zone(
        modules= Project1,            # module of second project
        # routes = Project1.home,     # if auto-detection is off
        # shared = Project1.shared,   # if auto-detection is off
        # path = 'project'            #if auto-naming is off
            )
ft.run(fy.fly)