import asyncio
import flet as ft
import fletfly as fy

@fy.Shared(value='I am shared, change me') # auto named to 'CardDeck'
@fy.Shared('CardDeck2', value='I am shared, change me too')
class CardDeck(ft.TextField): pass

class Home(fy.Route):
    def layout(self, page):    # Auto-detected layout by names (layout, frame)
        return ft.Column([
            fy.slot(page, "CardDeck", shared=True), # stuck always
            fy.slot(page) ])
    def view(self): return 'CardDeck2'     # Shared but delivered by view
class A(fy.Route):
    class B:
        class C:
            class D:
                class E:
                    def layout(self, page):
                        return ft.Column([
                            fy.slot(page, "CardDeck", shared=True),
                            fy.slot(page, "CardDeck2", shared=True)
                        ])
async def main(page):
    fy.fly(page)
    target_pages = ['home', 'a/b/c/d/e']
    for _ in range(10):
        for p in target_pages:
            await asyncio.sleep(5)
            page.fly(p)
ft.run(main)