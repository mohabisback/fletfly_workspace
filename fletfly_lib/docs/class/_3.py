import flet as ft
import fletfly as fy
# will not be registered by decoration

class Home(fy.Route):               # will not be registered by inheritence
    path = 'home'
    def layout(self):               # will not be detected by name
        pass
    check = fy.fly_in(lambda _: True)  # will not be detected by value
    
    def settings(self):             # Method will not create a subroute
        pass
    class User:                     # Inner class will not create a subroute
        pass

class CardDeck(fy.Shared):              # will not be registered by creation
    name = 'shared'                 # will not be auto named
fy.Router(
    routes=[Home],                  # Class Registered explicitly
    shared=[CardDeck],                # Class Registered explicitly 
    initial_route = "/",            # don't let us detect the initial for you
    error_path = "",                # don't let us show our error page, tell us where
    auto_path_naming=False,         # don't let us name your paths
    detect_route_subclasses=False,  # don't let us gather your routes inheriting from Route
    detect_method_routes=False,     # don't let us detect methods as subroutes
    detect_inner_classes=False,     # don't let us detect your inner classes as subroutes
    detect_method_ordinaries=False, # don't let us detect methods as props by name or value
    detect_shared=False)            # don't let us gather your shared
def main(page):
    fy.fly(page)
if __name__ == "__main__":
    ft.run(main)