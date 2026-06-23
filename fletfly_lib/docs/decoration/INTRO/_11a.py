import flet as ft
import fletfly as fy 

shared = fy.Shared()
@shared.use.view(hero=True, value='I am "CardDeck" shared of Sub Project')
class CardDeck(ft.TextField): pass

home = fy.Route()

@home.use.view
def sub_home_view():
    return (
        ft.Text("Sub project Home page"),
        ft.Button('Go settings', on_click=lambda e: e.page.fly('home/settings')),
        ft.Button('Go Root Home', on_click=lambda e: e.page.fly('home', root=True)),
        'CardDeck'
    )

settings = fy.Route()

@settings.use.view
def settings_view(page):
    return (
        ft.Text("Sub project Settings page"),
        ft.Button('Go Home', on_click=lambda e: e.page.fly('home')),
        ft.Button('Go Root Home', on_click=lambda e: e.page.fly('home', root=True)),
        'CardDeck'
    )

home.children.append(settings)

if __name__ == "__main__":
    ft.run(fy.fly)