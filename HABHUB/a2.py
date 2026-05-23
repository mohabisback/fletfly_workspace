class Airway:
    fly_in = ["class"] 

    def __init__(self, fly_in=None):
        self.fly_in = fly_in


instance_a = Airway(['a'])
instance_b = Airway(['b'])

instance_a.fly_in.append("AuthMiddleware")

print(f"Instance A: {instance_a.fly_in}")
print(f"Instance B: {instance_b.fly_in}")
print(f"Original Class: {Airway.fly_in}")