import flet as ft
import time
import threading

def _apply_lazy_loader(page, layout_view_func, lazy_loader_func=None):

    page.fly._temp_data = []
    controls_s = layout_view_func(page)

    captured = page.fly._temp_data.copy()

    if lazy_loader_func and captured:

        def lazy_worker(registry_snapshot):    
            data = lazy_loader_func()
            
            for item in registry_snapshot:
                attrs = item['map']
                control = item["control"]
                
                for attr, data_path in attrs.items():                    
                    raw_value = _get_nested_value(data, data_path)
                    final_value = validate_and_rescue(control, attr, raw_value)
                    if final_value is not None:
                        setattr(control, attr, final_value)
                
            page.update()
        threading.Thread(target=lazy_worker, args=(captured,), daemon=True).start()

    return controls_s

def _get_nested_value(data, path_str):
    if not path_str or path_str.strip() == "": # requested data = "" | None
        return data

    keys = path_str.split(".")
    current = data
    
    accumulated_path = ""
    
    for key in keys:
        is_numeric = key.isdigit()
        
        current_path = f"{accumulated_path}.{key}" if accumulated_path else key
        
        if isinstance(current, (list, tuple)):
            if is_numeric:
                try:
                    current = current[int(key)]  # requested data = "0" | "users_list.0"
                except IndexError:
                    print(f"⚠️  [FletFly Data]: {current_path} index is out of range!")
                    return None
            else:
                print(f"⚠️  [FletFly Data]: {current_path} expected an integer index, but got string!")
                return None
                
        elif isinstance(current, dict):
            if is_numeric:                   # requested data = "0" | "users_dict.0"
                int_key = int(key)
                if int_key in current:          
                    current = current[int_key]  # data = {0:"name"} | {"users_dict":{0:"name"}}
                elif key in current:
                    current = current[key]   # data = {"0":"name"} | {"users_dict":{"0":"name"}}
                else:
                    print(f"⚠️  [FletFly Data]: Inside data, key '{current_path}' (int or str) was not found!")
                    return None
            else:
                if key in current:
                    current = current[key]
                else:
                    print(f"⚠️  [FletFly Data]: Inside data, key '{current_path}' was not found!")
                    return None
                    
        else:
            print(f"⚠️  [FletFly Warning]: Inside data, the path '{accumulated_path}' is not a valid dictionary or list to look up '{key}'!")
            return None
        
        accumulated_path = accumulated_path + "." + key if accumulated_path else key
            
    return current
def validate_and_rescue(control, attr: str, new_value) -> any:
    """
    Validates and casts incoming data based on Flet 0.86 strict hierarchy,
    returning the clean value directly to be injected into the control attribute.
    """
    annotation = type(control).__annotations__.get(attr)
    allowed_types = annotation.__args__ if hasattr(annotation, "__args__") else (annotation,)
    
    actual_type = type(new_value)

    # 1. Initial Check: Is it perfectly valid as-is?
    if actual_type == annotation or actual_type in allowed_types:
        return new_value

    # 2. Float Casting Check
    elif float in allowed_types and type(new_value) in (int, str):
        try:
            return float(new_value)
        except (ValueError, TypeError):
            pass

    # 3. Integer Casting Check
    elif int in allowed_types and type(new_value) in (float, str):
        try:
            return int(float(new_value))
        except (ValueError, TypeError):
            pass

    # 4. String Casting Check
    elif str in allowed_types:
        try:
            return str(new_value)
        except (ValueError, TypeError, AttributeError):
            pass

    # 5. Final Line of Defense: UI Rescue fallback values
    if bool in allowed_types:
        return False
    print(f"⚠️ [fletfly data]: The value passed to '{attr}' doesn't match attr type and can't be casted")
    return None

def data(page: ft.Page, control, **kwargs):
    data_msg=f"""
[fletfly data] you must apply a lazy_loader function returning the lazy data, and use data() as following:
fty.data(page,
    ft.Text(size=24, weight="bold"),   # your ft.Control
    value=("user.name", "loading..."), # with default, extracted from data {"{'user':{'name':'your_name'}}"}  
    color=("user.0")                   # without default, extracted from data {"{'user':['red']}"}
)
Hint: you can use flet auto complete first for the **kwargs, then move the ) up to separate the control
"""
    if not control or not kwargs:
        print(data_msg)
        return control
        
    attr_map = {}
    for attr, config in kwargs.items():
        val = None  
        default_val = None
        if isinstance(config, (tuple,list)):
            config_len = len(config)
            if config_len < 1:
                print(data_msg)
                continue
            elif config_len < 2:
                val = config[0]
            elif config_len == 2:
                val, default_val = config
            else:
                print(data_msg)
        elif isinstance(config, str):
            val = config
        elif isinstance(config, (int, float)):
            val = str(config)
        else:
            print(data_msg)   
        if val is not None:
            attr_map[attr] = val
            if default_val is not None:
                try:           
                    setattr(control, attr, default_val)
                except: # flet will aready send an attr error
                    print(data_msg)
    if attr_map:
        page.fly._temp_data.append({"control": control, "map":attr_map})
    return control

import time
import fletfly as fty

def loader():

    time.sleep(3)
    
    # بناء الديكشنري بـ 100 منتج
    data = {"products": []}
    for i in range(200):
        data["products"].append({
            "name": f"Product {i + 1}",
            "price": f"{ (i + 1) * 10 }$"
        })
    
    return data
     


def view(page): 

    grid = ft.GridView(expand=True, max_extent=200, spacing=10)
    
    for i in range(200):

        name_txt = ft.Text(size=16, weight="bold")
        price_txt = ft.Text(size=14, color="green")
        
        data(page, name_txt, value=f"products.{i}.name")
        data(page, price_txt, value=f"products.{i}.price")
        
        grid.controls.append( 
            ft.Card(content=ft.Column([name_txt, price_txt], alignment=ft.Alignment.CENTER))
        )
    return grid  
  

fty.Router(fty.Route("/", view, loader=loader))
def main(page):   
    fty.fly(page, "/")
     
ft.run(main=main) 