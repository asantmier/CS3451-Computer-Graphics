# Ray data
class Ray:
    # origin and direction are PVectors
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
    
    def evaluate(self, t):
        return self.origin + (t * self.direction)
    
    def __repr__(self):
        return "Ray from {} in direction {}".format(self.origin, self.direction)
