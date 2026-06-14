import flet as ft
import flet_charts as fc

# 1. A direct instance from the flet_charts library
chart_instance = fc.PieChart()
line = fc.LineChart()
print(111111111111111, isinstance(line, ft.Control))
# 2. A custom user-defined class inheriting from an external Flet extension
class MyCustomDashboard(fc.LineChart):
    pass

dashboard_instance = MyCustomDashboard()

# ----------------------------------------------------------------------
# The Routing Engine Verification Logic
# ----------------------------------------------------------------------
def analyze_control(value):
    # Get the class type whether given an instance or the class itself
    cls = value if isinstance(value, type) else type(value)
    
    print(f"\n[Inspecting Control]: {cls.__name__}")
    print(f"  - Direct __module__: '{cls.__module__}'")
    print(f"  - Full __mro__ Family Tree:")
    
    is_flet_system = False
    
    # Fast path for core Flet controls
    if isinstance(value, ft.Control):
        is_flet_system = True
    
    # Fallback to inspect the ancestral lineage
    for base in getattr(cls, "__mro__", []):
        base_mod = getattr(base, "__module__", "")
        print(f"    <- Ancestor: {base.__name__:<20} | Defined in Module: {base_mod}")
        
        # Catch any ancestor belonging to core flet or external flet packages
        if base_mod and (base_mod.startswith("flet") or "flet" in base_mod):
            is_flet_system = True
            
    print(f"  ==> ENGINE DECISION: Is this a valid Flet component? -> {is_flet_system}")

# Run the live test
analyze_control(line)
analyze_control(dashboard_instance)