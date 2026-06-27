import asyncio
import flet as ft
import fletfly as fy

class Workspace(fy.Route):
    path = "workspace"
    
    def layout(self, page): # Persistent layout: Reconciled and never rebuilt from scratch
        return ft.Column([
            ft.Text("Workspace Shared Layout", size=20, weight="bold"),
            ft.TextField(label="Type here to test state retention"), 
            fy.slot(page)
        ])

    class Profile:
        path = ":id"
        created_count = 0 # Global class counters for explicit memory audit
        destroyed_count = 0

        def __init__(self):
            Workspace.Profile.created_count += 1
            self._print_audit("Born")
            
        def __del__(self):
            Workspace.Profile.destroyed_count += 1
            self._print_audit("Dead")

        def _print_audit(self, event):
            active = Workspace.Profile.created_count - Workspace.Profile.destroyed_count
            try:
                print(f"[Memory Audit] Event: {event:<4} | Created: {Workspace.Profile.created_count:<3} | Destroyed: {Workspace.Profile.destroyed_count:<3} | Active in Heap: {active}")
            except OSError:
                pass # Ignore I/O errors during interpreter shutdown
        def view(self, id):
            return ft.Text(f"Profile Content ID: {id}")

async def main(page):
    fy.fly(page, 'workspace/0')
    await asyncio.sleep(5) # time to type and test retention
    for i in range(1, 50): # Simulating 50 sequential transitions to audit memory stability
        await asyncio.sleep(0.05)
        fy.fly(page, f"workspace/{i}")

ft.run(main)