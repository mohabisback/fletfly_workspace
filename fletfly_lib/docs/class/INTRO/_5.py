import flet as ft
import fletfly as fy

class Home(fy.Route):                  
    def layout(self, page):    
        return ft.Column([
            ft.Text("Header"),
            fy.slot(page),        # Anonymous slot (ordered injection)
            fy.slot(page, 1),     # named slot (specific injection)
            fy.slot(page, 'a'),   # named slot (specific injection)
            fy.slot(page, control=ft.Card()), # default=ft.Container
            fy.slot(page, "CardDeck", shared=True) # stuck always to shared view named "CardDeck"
        ])
    def view(self):
        return(
            {1: ft.Text("Going for slot called 1")},
            {'a': ft.Text("Going for slot called a")},
            ft.Text("Going for first nameless slot"),
            ft.Text("Going for second nameless slot"),
            ft.Text("Have no where to go")
            )
@fy.Shared(value='I am shared')
class CardDeck(ft.TextField): pass

ft.run(fy.fly)            
