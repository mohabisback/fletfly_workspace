import flet as ft
import fletfly as fy

@fy.Shared(hero=True, value = 'I am "CardDeck" shared of Sub Project')
class CardDeck(ft.TextField): pass

class Home(fy.Route):
    path = '/home'
    def view(self):
        return (
            ft.Text ("Sub project Home page"),
            ft.Button('Go settings', on_click=lambda e: fy.fly(e.page, 'home/settings')),
            ft.Button('Go Root Home', on_click=lambda e: fy.fly(e.page, 'home', root=True)),
            'CardDeck'
        )
    class Settings:
        path = '/home/settings'
        def view(self):
            return (
                ft.Text ("Sub project Settings page"),
                ft.Button('Go Home', on_click=lambda e: fy.fly(e.page, 'home')),
                ft.Button('Go Root Home', on_click=lambda e: fy.fly(e.page, 'home', root=True)),
                'CardDeck'
            )
if __name__ == "__main__":
    ft.run(fy.fly)