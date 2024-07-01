from fastpvector import PVector
# Camera data
class Camera:
    def __init__(self):
        self.fov = 10 # obviously wrong number for debugging
    
    def set_eye(self, ex, ey, ez):
        self.eye = PVector(ex, ey, ez)
    
    def set_frame(self, ux, uy, uz, vx, vy, vz, wx, wy, wz):
        self.u = PVector(ux, uy, uz) # Rightward
        self.v = PVector(vx, vy, vz) # Upward
        self.w = PVector(wx, wy, wz) # Backward
