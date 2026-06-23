import asyncio
import flet as ft
import fletfly as fy

class CardDeck(ft.TextField): pass

# Auto detected and added
fy.Shared({
    "view": CardDeck,
    "value": 'I am shared, change me'
})

# Explicitly registered via Router
CardDeck2 = {
    "name": "CardDeck2",
    "view": CardDeck,
    "props": {
        "value": 'I am shared, change me too'
    }
}

def home_layout(page):
    return ft.Column([
        fy.slot(page, "CardDeck", shared=True),
        fy.slot(page) 
    ])

def home_view(): 
    return 'CardDeck2'

def e_layout(page):
    return ft.Column([
        fy.slot(page, "CardDeck", shared=True),
        fy.slot(page, "CardDeck2", shared=True)
    ])

# --- Home Route Dict ---
home = {
    "path": "home",
    "layout": home_layout,
    "view": home_view
}

# --- Deep Nested Route Dict ---
e = {
    "path": "a/b/c/d/e",
    "layout": e_layout
}

# Registering routes and explicit shared components
fy.Router([home, e], shared=[CardDeck2])

async def main(page):
    fy.fly(page)
    target_pages = ['home', 'a/b/c/d/e']
    for _ in range(10):
        for p in target_pages:
            await asyncio.sleep(2)
            page.fly(p)

ft.run(main=main)