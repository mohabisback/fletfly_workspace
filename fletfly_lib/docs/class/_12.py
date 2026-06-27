import flet as ft
import fletfly as fy


class A(fy.Route):
    @fy.child('b')  
    class B: pass

    @fy.child('c')
    def c(): pass

    @fy.index      
    class D:
        def view(self): return ft.Text("This is index D")
    
    @fy.index      
    def e(): return ft.Text("This is index e")

class F(fy.Route):
    def view(self): return ft.Text("This is index F")
class G(fy.Route):
    class Child1: pass
    def child2(): pass

    class Index:      # only if detect_inner_classes is True
        def view(self): return ft.Text("This is index G")
    def index(self):  # only if detect_method_routes is True
        return ft.Text("This is index g")
    

class X(fy.Route):
    child1 = A
    index = F

ft.run(fy.fly)