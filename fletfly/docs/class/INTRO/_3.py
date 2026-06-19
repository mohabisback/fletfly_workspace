import flet as ft
from fletfly import Router, Route, fly, fly_in
# will not be registered by decoration
@Route('home')                      # explicit paths only
class Home(Route):                  # will not be registered by inheritence

    def layout(self):               # will not be detected by name
        pass
    check = fly_in(lambda _: True)  # will not be detected by value
    
    def settings(self):             # Method will not create a subroute
        pass
    class User:                     # Inner class will not create a subroute
        pass
    
Router(
    routes=[Home],                  # Class Registered explicitly
    initial_route = "/",            # don't let us detect the initial for you
    error_path = "",                # don't let us show our error page, tell us where
    auto_path_naming=False,         # don't let us name your paths
    detect_route_subclasses=False,  # don't let us gather your routes inheriting from Route
    detect_method_routes=False,     # don't let us detect methods as subroutes
    detect_inner_classes=False,     # don't let us detect your inner classes as subroutes
    detect_method_ordinaries=False) # don't let us detect methods as props by name or value

def main(page):
    fly(page)
if __name__ == "__main__":
    ft.run(main)