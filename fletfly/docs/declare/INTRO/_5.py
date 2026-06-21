import flet as ft
import fletfly as fy 

def layout(page):    
    return ft.Column([
        ft.Text("Header"),
        fy.slot(page),        # Anonymous slot (ordered injection)
        fy.slot(page, 1),     # named slot (specific injection)
        fy.slot(page, 'a'),   # named slot (specific injection)
        fy.slot(page, control=ft.Card()), # default=ft.Container
        fy.slot(page, "CardDeck", shared=True) # stuck always to shared view named "CardDeck"
    ])

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

shared = fy.Shared(CardDeck, value='I am shared')

# Declarative tree composition
home = fy.Route(
    fy.use.layout(layout),
    fy.use.view(view)
)

ft.run(fy.fly)