import flet as ft
import fletfly as fy
from _11a import Home as Project1

@fy.Shared(value = 'I am "CardDeck" shared of Main Zone')
class CardDeck(ft.TextField): pass

class Home(fy.Route): # Main project '/home'
    def view(self): return (
                ft.Text ("Main Home page"),
                ft.Button("Go Sub Project", on_click=lambda e: e.page.fly('home/project')),
                'CardDeck' )
    
    Project = fy.Zone(Project1) # Zone, auto named to '/home/project'

ft.run(fy.fly)