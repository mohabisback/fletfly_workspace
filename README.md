> 💡 **Note:** This is the workspace for the [`fletfly`](./fletfly) library project.

# fletfly
**The Component Composition Engine for Flet.**

"Stop writing procedural routing logic. `fletfly` injects data into your builds, nests views and shared components into multi-layered layouts, reconciles the tree, and preserves state—all with built-in middlewares, microfrontend nav and zero boilerplate."

---
> 💡 **Polyglot Design:** `fletfly` adapts to your coding model. The core engine is unified, but the syntax is yours to choose.
>
> **Choose your weapon:**
>
> * **[Class-Based](fletfly/docs/class/INTRO.md)** — *Django, Flutter, ASP.NET*
> * **[Registry/Dictionary](fletfly/docs/dict/INTRO.md)** — *Vue, Express, Angular*
> * **[Declarative](fletfly/docs/declare/INTRO.md)** — *React, SwiftUI, Flutter Trees*
> * **[File-Based](fletfly/docs/file/INTRO.md)** — *Next.js, Nuxt.js, SvelteKit*
> * **[Decorator-Based](fletfly/docs/decoration/INTRO.md)** — *FastAPI, Flask, NestJS*

--- 
 📌 **Note:** This guide uses **Class-Based Routing** as our primary example to demonstrate the engine's hierarchical power. You can find dedicated guides for other paradigms in their respective directories.
---

## The 20-Line Engine Shock
Look at this single block of code. It demonstrates auto-pathing (static & dynamic), dynamic (nameless) slot injection, and hierarchical layout inheritance—all without a single manual routing string or `page.add()` call.

```python
from fletfly import Airway, slot
import flet as ft

@Airway
class Home:                                  # 1. Auto-path detection ("/home")
    def layout(page):                        # 2. Inheritable layout structure
        return ft.Column([
            ft.Text("Header"),
            slot(page),                      # Injected Content 1
            slot(page),                      # Injected Content 2
            ft.Text("Footer")
        ])
        
    def build(page):                         # 3. Content for "/home"
        return (
            ft.Text("Hi"),                   # Fills Content 1
            ft.Text("Welcome home")          # Fills Content 2
        )

    @Airway(":id")                           # 4. Auto-resolves to "/home/:id"
    class User:
        def build(page):
            # 5. Inherits Home layout automatically!
            return (
                ft.Text("User profile:"),              # Fills Content 1
                ft.Text(f"{page.params['id']}")        # Fills Content 2
            )
```

2. Layout Overrides
Break the inheritance gracefully when you need an isolated view (like a login or settings page) within a nested structure.

```python
    @Airway("settings", layout_override=True)
    class Settings:
        def layout(page):
            # This layout acts as a new root, ignoring the parent's structure
            return ft.Row([slot(page)])

        def build(page):
            return ft.Text("Settings Panel")
```