from fletfly import Route, slot, fly, Shared
import flet as ft

home = Route()

@home.at.layout
def layout(page):    
    return ft.Column([
        ft.Text("Header"),
        slot(page),        # Anonymous slot (ordered injection)
        slot(page, 1),     # named slot (specific injection)
        slot(page, 'a'),   # named slot (specific injection)
        slot(page, control=ft.Card()), # default=ft.Container
        slot(page, "CardDeck", shared=True) # stuck always to shared view named "CardDeck"
    ])

@home.at.view
def view():
    return (
        {1: ft.Text("Going for slot called 1")},
        {'a': ft.Text("Going for slot called a")},
        ft.Text("Going for first nameless slot"),
        ft.Text("Going for second nameless slot"),
        ft.Text("Have no where to go")
    )

def CardDeck(value): 
    return ft.TextField(value)

shared = Shared(CardDeck, value='I am shared')

ft.run(fly)