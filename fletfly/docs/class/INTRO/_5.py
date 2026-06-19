from fletfly import Route, slot, fly, Shared
import flet as ft

class Home(Route):                  
    def layout(self, page):    
        return ft.Column([
            ft.Text("Header"),
            slot(page),        # Anonymous slot (ordered injection)
            slot(page, 1),     # named slot (specific injection)
            slot(page, 'a'),   # named slot (specific injection)
            slot(page, control=ft.Card()), # default=ft.Container
            slot(page, "CardDeck", shared=True) # stuck always to shared view named "CardDeck"
        ])
    def view(self):
        return(
            {1: ft.Text("Going for slot called 1")},
            {'a': ft.Text("Going for slot called a")},
            ft.Text("Going for first nameless slot"),
            ft.Text("Going for second nameless slot"),
            ft.Text("Have no where to go")
            )
@Shared(value='I am shared')
class CardDeck(ft.TextField): pass

ft.run(fly)            
