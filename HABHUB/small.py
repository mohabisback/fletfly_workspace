import flet as ft

# --------------------------------------------------------------------
# THE CORE FLETFLY DECORATOR (YOUR ENGINE STRUCTURE)
# --------------------------------------------------------------------
def fly_around(*args, **kwargs):
    # Case 1: @fly_around حاف on Class
    if len(args) == 1 and isinstance(args[0], type):
        print(f"[CASE 1] Bare Class detected: '{args[0].__name__}' registered via Auto-naming.")
        return args[0]
        
    # Case 2: @fly_around حاف on Function
    elif len(args) == 1 and callable(args[0]):
        print(f"[CASE 2] Bare Function detected: '{args[0].__name__}' registered via Auto-naming.")
        return args[0]
        
    # Outer Else for Arguments / Placeholder calls (Cases 3, 4, 5)
    else:
        # Save the custom name if passed, e.g., @fly_around("name")
        custom_name = args[0] if args else None

    def wrapper(cls_or_func):
        # Case 3: @fly_around("name") on Class
        if isinstance(cls_or_func, type):
            print(f"[CASE 3] Class with args detected: '{cls_or_func.__name__}' registered with custom name: '{custom_name}'.")
            return cls_or_func
            
        # Case 4: @fly_around("name") on Function
        elif callable(cls_or_func):
            print(f"[CASE 4] Function with args detected: '{cls_or_func.__name__}' registered with custom name: '{custom_name}'.")
            
            # The Runtime Inception Wrapper
            def func(page: ft.Page, *run_args, **run_kwargs):
                if not page or not isinstance(page, ft.Page):
                    raise ValueError("[fletfly] A build, shared or layout function must have a page:ft.Page argument")
                print(f"   ==> [Runtime Success] Inside '{cls_or_func.__name__}' execution! ft.Page validated successfully.")
                return cls_or_func(page, *run_args, **run_kwargs)
                
            return func
            
        # Case 5: Placeholder logic (Engine calls wrapper with non-callable placeholder token)
        else:
            print(f"[CASE 5] Placeholder Shit triggered! Received Token: '{cls_or_func}'. Creating/Returning Shared Object later.")
            return "SHARED_OBJECT_MOCK"

    return wrapper

# --------------------------------------------------------------------
# SIMULATING THE 5 CASES
# --------------------------------------------------------------------
print("--- STARTING APP INITIALIZATION (IMPORT TIME) ---\n")

# --- Test Case 1 ---
@fly_around
class MainLayoutClass:
    pass

# --- Test Case 2 ---
@fly_around
def main_build_func(page: ft.Page):
    pass

# --- Test Case 3 ---
@fly_around("custom_profile_view")
class ProfileClass:
    pass

# --- Test Case 4 ---
@fly_around("custom_navbar")
def navbar_func(page: ft.Page):
    print("       Executing original navbar_func logic...")

print("\n--- APP INITIALIZED. SIMULATING RUNTIME (ROUTER & ENGINE WORK) ---\n")

def main(page):
    # --- Executing Case 4 Runtime (Router invokes the wrapped function with a mock Page)
    print("Action: Router is now calling navbar_func...")
    navbar_func(page) 

    print("-" * 50)

    # --- Test Case 5 (How your Engine resolves a Placeholder behind the scenes)
    print("Action: User writes fly_around('sidebar') in Layout. Engine intercepts the wrapper...")
    captured_wrapper = fly_around("sidebar") # What the user code returns implicitly

    print("Action: Engine invokes the captured wrapper with a special engine_token...")
    resolved_node = captured_wrapper("ENGINE_PLACEHOLDER_TOKEN") # Engine enforces Case 5
    print(f"Result: Engine successfully retrieved -> {resolved_node}")

    print("\n--- TEST FINISHED SUCCESSFULLY ---")

ft.run(main)