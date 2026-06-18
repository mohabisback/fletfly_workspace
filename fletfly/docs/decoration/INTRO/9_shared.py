from fletfly import Route, slot, fly, Shared
import flet as ft
import asyncio

@Shared(value='I am shared, change me') # auto named to 'CardDeck'
@Shared('CardDeck2', value='I am shared, change me too')
class CardDeck(ft.TextField): pass

class Home(Route):
    def layout(self, page):    # Auto-detected layout by names (layout, frame)
        return ft.Column([
            slot(page, "CardDeck", shared=True), # stuck always
            slot(page) ])
    def view(self): return 'CardDeck2'     # Shared but delivered by view
class A(Route):
    class B:
        class C:
            class D:
                class E:
                    def layout(self, page):
                        return ft.Column([
                            slot(page, "CardDeck", shared=True),
                            slot(page, "CardDeck2", shared=True)
                        ])
async def main(page):
    fly(page)
    target_pages = ['home', 'a/b/c/d/e']
    for _ in range(5):
        for p in target_pages:
            await asyncio.sleep(5)
            page.fly(p)
ft.run(main)