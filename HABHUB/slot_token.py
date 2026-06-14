import sys

# Simulation of page.fly._slots_token
active_token = None

def slot():
    """
    Simulates your slot() function behavior using sys._getframe
    """
    fr = sys._getframe(1)
    func_key = f"{fr.f_code.co_filename}::{fr.f_code.co_qualname}"
    
    print(f"  [Slot Side]   Generated Key: {func_key}")
    
    if func_key == active_token:
        print("  [Slot Side]   Verification: MATCH SUCCESS (Authorized)")
    else:
        print("  [Slot Side]   Verification: MATCH FAILED (Unauthorized)")

def engine_execute(func):
    """
    Simulates the Router Engine executing the loader with 4-way inspection logic
    """
    global active_token
    
    # 1. Full Class Type (__init__)
    if isinstance(func, type):
        target_code = func.__init__.__code__
        strategy = "Class Constructor (__init__)"
        
    # 2. Callable Instance (__call__)
    elif hasattr(func, '__call__') and not hasattr(func, '__code__'):
        target_code = func.__call__.__code__
        strategy = "Callable Instance (__call__)"
        
    # 3. Bound Method (instance.method)
    elif hasattr(func, '__func__'):
        target_code = func.__func__.__code__
        strategy = f"Bound Method ({func.__name__})"
        
    # 4. Standalone Function
    else:
        target_code = func.__code__
        strategy = f"Standalone Function ({func.__name__})"
        
    func_key = f"{target_code.co_filename}::{target_code.co_qualname}"
    print(f"\n[Engine Side] Detected Type: {strategy}")
    print(f"[Engine Side] Target Token Set: {func_key}")
    
    active_token = func_key
    
    # Trigger execution dynamically
    func()  
        
    active_token = None

# ==========================================
# TEST CASES
# ==========================================

# 1. Standalone Function
def standalone_loader():
    slot()

# 2. Bound Method inside a Class
class MyView:
    def method_loader(self):
        slot()

# 3. Full Class (Triggers __init__)
class MyClassComponent:
    def __init__(self):
        slot()

# 4. Callable Instance (Triggers __call__)
class MyCustomCallable:
    def __call__(self):
        slot()

# ==========================================
# EXECUTION
# ==========================================

if __name__ == "__main__":
    print(f"Current Python Version: {sys.version.split()[0]}")
    
    # Test 1: Function
    print("-" * 65)
    engine_execute(standalone_loader)
    
    # Test 2: Method
    print("-" * 65)
    view_instance = MyView()
    engine_execute(view_instance.method_loader)
    
    # Test 3: Full Class
    print("-" * 65)
    engine_execute(MyClassComponent)
    
    # Test 4: Callable Instance
    print("-" * 65)
    callable_obj = MyCustomCallable()
    engine_execute(callable_obj) # Invoking the object directly
    print("-" * 65)