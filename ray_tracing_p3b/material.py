# Material data
class Material:
    def __init__(self, dr, dg, db, ar, ag, ab, sr, sg, sb, spec_power, k_refl):
        self.diffuseColor = (dr, dg, db)
        self.ambientColor = (ar, ag, ab)
        self.specularColor = (sr, sg, sb)
        self.specularPower = spec_power
        self.k_refl = k_refl
        
    def __repr__(self):
        return "Diffuse {}, Ambient {}, Specular {} power = {}, Reflection k = {}".format(
                    self.diffuseColor, self.ambientColor, self.specularColor, self.specularPower, self.k_refl)
