import asyncio
from fletfly import Router, Route, slot, fly, Shared
import flet as ft

class CardDeck(ft.TextField): pass
shared = Shared(CardDeck, value='I am shared, change me') # auto-named to CardDeck
CardDeck2 = Shared(CardDeck, value='I am shared, change me too')

# --- Home Route ---
home = Route()

@home.at.layout
def home_layout(page):    # Auto-detected layout
    return ft.Column([
        slot(page, "CardDeck", shared=True), # stuck always
        slot(page) 
    ])

@home.at.view
def home_view(): 
    return 'CardDeck2'     # Shared but delivered by view


# --- Deep Nested Route (a/b/c/d/e) ---
e = Route('/a/b/c/d/e')

@e.at.layout
def e_layout(page):
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

ft.run(main=main)