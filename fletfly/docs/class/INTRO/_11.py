import flet as ft
from fletfly import Route, Zone, fly, Shared
from _11a import Home as Project1

@Shared(value = 'I am "CardDeck" shared of Main Zone')
class CardDeck(ft.TextField): pass

class Home(Route): # Main project '/home'
    def view(self): return (
                ft.Text ("Main Home page"),
                ft.Button("Go Sub Project", on_click=lambda e: e.page.fly('home/project')),
                'CardDeck' )
    
    Project = Zone(Project1) # Zone, auto named to '/home/project'

ft.run(fly)