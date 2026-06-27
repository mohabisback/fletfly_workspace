import asyncio
import flet as ft
import fletfly as fy

shared = fy.Shared() # auto-named to CardDeck
CardDeck2 = fy.Shared()

@shared.use.view(value='I am shared, change me')
@CardDeck2.use.view(value='I am shared, change me too')
class CardDeck(ft.TextField): pass

# --- Home Route ---
home = fy.Route()

@home.use.layout
def home_layout(page):    # Auto-detected layout
    return ft.Column([
        fy.slot(page, "CardDeck", shared=True), # stuck always
        fy.slot(page) 
    ])

@home.use.view
def home_view(): 
    return 'CardDeck2'     # Shared but delivered by view


# --- Deep Nested Route (a/b/c/d/e) ---
e =fy.Route('/a/b/c/d/e')

@e.use.layout
def e_layout(page):
    return ft.Column([
        fy.slot(page, "CardDeck", shared=True),
        fy.slot(page, "CardDeck2", shared=True)
    ])

async def main(page):
    fy.fly(page)
    target_pages = ['home', 'a/b/c/d/e']
    for _ in range(10):
        for p in target_pages:
            await asyncio.sleep(2)
            fy.fly(page, p)

ft.run(main=main)