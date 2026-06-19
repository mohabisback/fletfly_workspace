import flet as ft
import fletfly as fy Router, Route, fly, fly_in

# will not be registered by creation
home = Route('home')                # explicit paths only

Router(
    routes=[home],                  # routes Registered explicitly
    initial_route = "/",            # don't let us detect the initial for you
    error_path = "",                # don't let us show our error page, tell us where
    auto_path_naming=False,         # don't let us name your paths
    detect_created_routes=False,    # don't let us gather your created routes
) # don't let us detect methods as props by name or value

def main(page):
    fly(page)
if __name__ == "__main__":
    ft.run(main)