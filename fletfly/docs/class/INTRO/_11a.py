import flet as ft
from fletfly import Route, fly, Shared

@Shared(hero=True, value = 'I am "CardDeck" shared of Sub Project')
class CardDeck(ft.TextField): pass

class Home(Route):
    path = '/home'
    def view(self):
        return (
            ft.Text ("Sub project Home page"),
            ft.Button('Go settings', on_click=lambda e: e.page.fly('home/settings')),
            ft.Button('Go Root Home', on_click=lambda e: e.page.fly('home', root=True)),
            'CardDeck'
        )
    class Settings:
        path = '/home/settings'
        def view(self, page):
            return (
                ft.Text ("Sub project Settings page"),
                ft.Button('Go Home', on_click=lambda e: e.page.fly('home')),
                ft.Button('Go Root Home', on_click=lambda e: e.page.fly('home', root=True)),
                'CardDeck'
            )
if __name__ == "__main__":
    ft.run(fly)