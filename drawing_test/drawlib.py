# Drawing Routines that are similar to those in OpenGL

from matrix_stack import *

verticies = []
projection = "o"
l = 0
r = 0
t = 0
b = 0
persp_fov = 0

def gtOrtho(left, right, bottom, top, near, far):
    global orth, projection, l, r, t, b
    l = left
    r = right
    t = top
    b = bottom
    # near and far are ignored
    orth = (left, right, top, bottom)
    projection = "o"
    
def gtPerspective(fov, near, far):
    global orth, projection, persp_fov
    persp_fov = fov
    # near and far are ignored
    projection = "p"

def gtVertex(x, y, z):
    global verticies
    verticies.append([x, y, z])

def gtBeginShape():
    global verticies
    verticies = []

def gtEndShape():
    global verticies, projection, l, r, t, b, persp_fov
    for vi in range(0, len(verticies), 2):
        x1, y1, z1 = verticies[vi]
        x2, y2, z2 = verticies[vi + 1]
        x1, y1, z1 = gtTransform(x1, y1, z1)
        x2, y2, z2 = gtTransform(x2, y2, z2)
        (proj_x1, proj_y1, proj_x2, proj_y2) = (0, 0, 0, 0)
        if projection == "o":
            proj_x1 = (float(x1 - l) / (r - l)) * width
            proj_x2 = (float(x2 - l) / (r - l)) * width
            proj_y1 = (float(t - y1) / (t - b)) * height
            proj_y2 = (float(t - y2) / (t - b)) * height
        else:
            rel_x1 = x1 / abs(z1)
            rel_x2 = x2 / abs(z2)
            rel_y1 = y1 / abs(z1)
            rel_y2 = y2 / abs(z2)
            k = tan(radians(persp_fov) / 2)
            proj_x1 = ((rel_x1 + k) / (2 * k)) * width
            proj_x2 = ((rel_x2 + k) / (2 * k)) * width
            # height - to account for y being in the top left
            proj_y1 = height - (((rel_y1 + k) / (2 * k)) * height)
            proj_y2 = height - (((rel_y2 + k) / (2 * k)) * height)
        
        line(proj_x1, proj_y1, proj_x2, proj_y2)
