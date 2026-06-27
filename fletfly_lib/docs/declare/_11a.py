import flet as ft
import fletfly as fy 

class CardDeck(ft.TextField): pass
shared = fy.Shared(CardDeck, hero=True, value='I am "CardDeck" shared of Sub Project')

def sub_home_view():
    return (
        ft.Text("Sub project Home page"),
        ft.Button('Go settings', on_click=lambda e: fy.fly(e.page, 'home/settings')),
        ft.Button('Go Root Home', on_click=lambda e: fy.fly(e.page, 'home', root=True)),
        'CardDeck'
    )

def settings_view():
    return (
        ft.Text("Sub project Settings page"),
        ft.Button('Go Home', on_click=lambda e: fy.fly(e.page, 'home')),
        ft.Button('Go Root Home', on_click=lambda e: fy.fly(e.page, 'home', root=True)),
        'CardDeck'
    )

home = fy.Route(
    fy.use.view(sub_home_view),
    children=[
        fy.Route('settings',
            fy.use.view(settings_view)
        )
    ]
)

if __name__ == "__main__":
    ft.run(fy.fly)