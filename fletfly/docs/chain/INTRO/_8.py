import asyncio
import flet as ft
import fletfly as fy

class CardDeck(ft.TextField): pass
shared = fy.Shared().view(CardDeck).props(value='I am shared, change me') # auto-named to CardDeck
CardDeck2 = fy.Shared().view(CardDeck).props(value='I am shared, change me too')

def home_layout(page):    # Auto-detected layout
    return ft.Column([
        fy.slot(page, "CardDeck", shared=True), # stuck always
        fy.slot(page) 
    ])

def home_view(): 
    return 'CardDeck2'     # Shared but delivered by view

def e_layout(page):
    return ft.Column([
        fy.slot(page, "CardDeck", shared=True),
        fy.slot(page, "CardDeck2", shared=True)
    ])

# Chaining style composition

# --- Home Route ---
home = fy.Route().layout(home_layout).view(home_view)

# --- Deep Nested Route (a/b/c/d/e) ---
e = fy.Route('/a/b/c/d/e').layout(e_layout)

async def main(page):
    fy.fly(page)
    target_pages = ['home', 'a/b/c/d/e']
    for _ in range(10):
        for p in target_pages:
            await asyncio.sleep(2)
            page.fly(p)

ft.run(main=main)