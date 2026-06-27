import gc
import asyncio
import flet as ft
import fletfly as fy

# Custom Flet control to audit the view's lifecycle directly in Chaining Style
class AuditedView(ft.Text):
    created_count = 0
    destroyed_count = 0

    def __init__(self, text, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        AuditedView.created_count += 1
        self._print_audit("Born")

    def __del__(self):
        AuditedView.destroyed_count += 1
        self._print_audit("Dead")

    def _print_audit(self, event):
        active = AuditedView.created_count - AuditedView.destroyed_count
        try:
            print(f"[View Audit] Event: {event:<4} | Created: {AuditedView.created_count:<3} | Destroyed: {AuditedView.destroyed_count:<3} | Active Views: {active}")
        except OSError:
            pass

route = fy.Route('workspace')\
    .layout(lambda page: ft.Column([
        ft.Text("Workspace Shared Layout", size=20, weight="bold"),
        ft.TextField(label="Type here to test state retention"), 
        fy.slot(page)
    ]))\
    .child(':id').view(lambda id: AuditedView(f"Profile Content ID: {id}"))

async def main(page):
    # 1. Initial navigation to establish the layout and first view
    fy.fly(page, "workspace/0")
    await asyncio.sleep(5) # Time allowed for the developer to type and test retention
    
    for i in range(1, 50): # 2. Stress testing memory with 50 sequential transitions
        await asyncio.sleep(0.1)
        fy.fly(page, f"workspace/{i}")
        gc.collect() # so python won't lazy collect garbage, don't use this in your app

ft.run(main)