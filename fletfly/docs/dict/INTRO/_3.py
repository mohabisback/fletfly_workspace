import flet as ft
import fletfly as fy 

# will not be registered by creation
home = {'path':'home'}              # explicit path only
shared = {'name':'shared'}          # explicit name only

fy.Router(
    routes=[home],                  # routes Registered explicitly
    shared=[shared],                # shared Registered explicitly
    initial_route = "/",            # don't let us detect the initial for you
    error_path = "",                # don't let us show our error page, tell us where
    auto_path_naming=False,         # don't let us name your paths
    detect_created_routes=False,    # don't let us gather your created routes
    detect_shared=False,            # don't let us gather your shared
)

def main(page):
    fy.fly(page)
if __name__ == "__main__":
    ft.run(main)