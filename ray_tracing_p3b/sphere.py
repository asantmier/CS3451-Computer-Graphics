from fastpvector import PVector
# Sphere data
class Sphere:
    
    def __init__(self, x, y, z, r, mat):
        self.center = PVector(x, y, z)
        self.radius = r
        self.material = mat
    
    def __repr__(self):
        return "Sphere at {}, R = {}. Material: {}".format(self.center, self.radius, self.material)
