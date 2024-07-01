from fastpvector import PVector
# Triangle data
class Triangle:
    
    def __init__(self, v1, v2, v3, mat):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.material = mat
        v1v2 = v2 - v1
        v2v3 = v3 - v2
        v3v1 = v1 - v3
        v1v3 = v3 - v1 # only for normal calculation
        # For some awful reason, the .cross function modifies the calling object, so we need to do this workaround
        U = PVector(v1v2.x, v1v2.y, v1v2.z)
        V = PVector(v1v3.x, v1v3.y, v1v3.z)
        # We are apparently given clockwise winding order
        self.normal = PVector.cross(V, U).normalize()
        self.edge1 = self.v2 - self.v1
        self.edge2 = self.v3 - self.v2
        self.edge3 = self.v1 - self.v3
        
    def half_plane_test(self, point):
        vp1 = point - self.v1
        # For some godforsaken reason, .cross modifies its caller, so we have to do this
        e = PVector(self.edge1.x, self.edge1.y, self.edge1.z)
        c = PVector.cross(e, vp1)
        if PVector.dot(self.normal, c) > 0: return False
    
        vp2 = point - self.v2
        e = PVector(self.edge2.x, self.edge2.y, self.edge2.z)
        c = PVector.cross(e, vp2)
        if PVector.dot(self.normal, c) > 0: return False
    
        vp3 = point - self.v3
        e = PVector(self.edge3.x, self.edge3.y, self.edge3.z)
        c = PVector.cross(e, vp3)
        if PVector.dot(self.normal, c) > 0: return False
        
        return True
    
    def __repr__(self):
        return "Triangle <{}, {}, {}>. Material: {}".format(self.v1, self.v2, self.v3, self.material)
