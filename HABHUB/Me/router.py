import flet as ft
from HABHUB.Me.home import get_view as get_home
from HABHUB.ImageResizer.router import router as get_ImageResizer
from HABHUB.Me.error import get_view as get_err

def startRouter(page: ft.Page):
    def route_change(firstRun=False):
        router(page, "/", firstRun) 
        page.update()

    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change(True)

def router(page, baseRoute:str="/", firstRun = False): #baseRoute = "/" | "/resizer" | "/anything"
    #resizer project
    if page.route == "/resizer" or page.route.startswith("/resizer/"):#to avoid "/resizer-2"
        get_ImageResizer(page, baseRoute="/resizer")
        return
    
    cleanRoute = baseRoute.strip("/")   
    Pages = {
            "base":baseRoute.rstrip("/")+"/",
            cleanRoute:{
                "":get_home,
                "error":get_err,
                "contact":{
                    "":get_home, #temp
                    "email":get_err, #temp
                    "phone":get_err, #temp
                        }
                }
            } 
    fullRoute = page.route.rstrip("/")
    if baseRoute not in ("", "/"): fullRoute = fullRoute.lstrip("/")
    target_segments = fullRoute.split("/")
    
    
    if firstRun:#first view ever
        page.views.clear()
        get_home(page, "/", Pages) #first view ever

    anchor_index = len(page.views) #start of similarity
    for i, view in enumerate(page.views):
        view_segments:list = view.route.rstrip("/").split("/")
        if view_segments[-1] == target_segments[0]: #first 
            anchor_index = i
            break

    #remove sure extra views
    while len(page.views)>anchor_index + len(target_segments):
        page.views.pop()

    currentRoute = ""
    currentDictOrVal = Pages
    for i, seg in enumerate(target_segments):
        if not isinstance(currentDictOrVal, dict) or not seg in currentDictOrVal :
            Pages[baseRoute.strip("/")]["error"](page, baseRoute.rstrip("/")+"/" + "error", Pages)
            break

        do_view = False
        if len(page.views)> anchor_index+i: #maybe similarity
                vw_segments:list = page.views[anchor_index+i].route.rstrip("/").split("/")
                if vw_segments[-1] == target_segments[i]:      #similarity
                    currentRoute = currentRoute.rstrip("/")+"/"+seg
                    currentDictOrVal = currentDictOrVal[seg]
                    continue #similarity
                else:                                          #no similarity
                    while len(page.views) > anchor_index+i:    #clean views
                        page.views.pop()
                    do_view = True
        else:
            do_view = True
        currentRoute = currentRoute.rstrip("/")+"/"+seg
        if do_view:    
            if isinstance(currentDictOrVal[seg], dict):     #view current view
                currentDictOrVal[seg][""](page, currentRoute, Pages)
            else:
                currentDictOrVal[seg](page, currentRoute, Pages)
            currentDictOrVal = currentDictOrVal[seg]
    page.update()
    print("Resize End of Views Function, count of page.views:", len(page.views))
    for i in range(len(page.views)):
        print(i, "route:", page.views[i].route)
