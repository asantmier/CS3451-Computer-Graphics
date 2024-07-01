# Material data
class Material:
    def __init__(self, dr, dg, db):
        self.diffuseColor = (dr, dg, db)
        
    def __repr__(self):
        return "Diffuse {}".format(self.diffuseColor)
