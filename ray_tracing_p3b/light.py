from fastpvector import PVector
# Light data
class Light:
    def __init__(self, x, y, z, r, g, b):
        self.pos = PVector(x, y, z)
        self.color = (r, g, b)
        
    def __repr__(self):
        return "Pos: {}, Color: {}".format(self.pos, self.color)
