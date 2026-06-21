import flet as ft
import fletfly as fy 

class CardDeck(ft.TextField): pass
shared = fy.Shared().view(CardDeck).hero(True).props(value='I am "CardDeck" shared of Sub Project')

def sub_home_view():
    return (
        ft.Text("Sub project Home page"),
        ft.Button('Go settings', on_click=lambda e: e.page.fly('home/settings')),
        ft.Button('Go Root Home', on_click=lambda e: e.page.fly('home', root=True)),
        'CardDeck'
    )

def settings_view():
    return (
        ft.Text("Sub project Settings page"),
        ft.Button('Go Home', on_click=lambda e: e.page.fly('home')),
        ft.Button('Go Root Home', on_click=lambda e: e.page.fly('home', root=True)),
        'CardDeck'
    )

home = fy.Route().view(sub_home_view)
home.child('settings').view(settings_view)

if __name__ == "__main__":
    ft.run(fy.fly)