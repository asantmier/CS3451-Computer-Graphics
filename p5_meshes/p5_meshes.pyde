# Provided code for Subdivison and Geodesic Spheres

from __future__ import division
import traceback
from random import randint, seed

# parameters used for object rotation by mouse
mouseX_old = 0
mouseY_old = 0
rot_mat = PMatrix3D()

G_table = []
V_table = []
O_table = []
random_color = False
random_seed = 0
frame = 0
current_corner = 0
disp_corner = True

# initalize things
def setup():
    size (800, 800, OPENGL)
    frameRate(30)
    noStroke()

# draw the current mesh (you will modify parts of this routine)
def draw():
    global G_table, V_table, O_table, random_color, random_seed, frame, current_corner, disp_corner
    frame += 1
    
    background (100, 100, 180)    # clear the screen to black

    perspective (PI*0.2, 1.0, 0.01, 1000.0)
    camera (0, 0, 6, 0, 0, 0, 0, 1, 0)    # place the camera in the scene
    
    # create an ambient light source
    ambientLight (102, 102, 102)

    # create two directional light sources
    lightSpecular (202, 202, 202)
    directionalLight (100, 100, 100, -0.7, -0.7, -1)
    directionalLight (152, 152, 152, 0, 0, -1)
    
    pushMatrix();

    stroke (0)                    # draw polygons with black edges
    fill (200, 200, 200)          # set the polygon color to white
    ambient (200, 200, 200)
    specular (0, 0, 0)            # turn off specular highlights
    shininess (1.0)
    
    applyMatrix (rot_mat)   # rotate the object using the global rotation matrix
    
    # THIS IS WHERE YOU SHOULD DRAW YOUR MESH
    seed(random_seed)
    for i in range(0, len(V_table) // 3):
        if random_color:
            fill (randint(0, 255), randint(0, 255), randint(0, 255))
        beginShape()
        v = G_table[V_table[(i * 3) + 0]]
        vertex (v[0],  v[1], v[2])
        v = G_table[V_table[(i * 3) + 1]]
        vertex (v[0],  v[1], v[2])
        v = G_table[V_table[(i * 3) + 2]]
        vertex (v[0],  v[1], v[2])
        endShape(CLOSE)
    
    if disp_corner and len(V_table) > 0:
        t = current_corner // 3
        # Corner's vertex
        vertx = G_table[V_table[current_corner]][0]
        verty = G_table[V_table[current_corner]][1]
        vertz = G_table[V_table[current_corner]][2]
        t = t * 3
        # Triangle center
        centerx = sum([G_table[V_table[t]][0], G_table[V_table[t + 1]][0], G_table[V_table[t + 2]][0]]) / 3
        centery = sum([G_table[V_table[t]][1], G_table[V_table[t + 1]][1], G_table[V_table[t + 2]][1]]) / 3
        centerz = sum([G_table[V_table[t]][2], G_table[V_table[t + 1]][2], G_table[V_table[t + 2]][2]]) / 3
        # Direction to center
        offx = centerx - vertx
        offy = centery - verty
        offz = centerz - vertz
        # Position of sphere
        posx = vertx + (.25 * offx)
        posy = verty + (.25 * offy)
        posz = vertz + (.25 * offz)
        noStroke()
        fill (200, 0, 0)
        translate(posx, posy, posz)
        sphere(.05)
    popMatrix()

# read in a mesh file (this needs to be modified)
def read_mesh(filename):
    global G_table, V_table, O_table, current_corner
    # Reset the corner's representation
    G_table = []
    V_table = []
    O_table = []
    current_corner = 0
    
    fname = "data/" + filename
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()

    # determine number of vertices (on first line)
    words = lines[0].split()
    num_vertices = int(words[1])
    print "number of vertices =", num_vertices

    # determine number of faces (on first second)
    words = lines[1].split()
    num_faces = int(words[1])
    print "number of faces =", num_faces

    # read in the vertices
    for i in range(num_vertices):
        words = lines[i+2].split()
        x = float(words[0])
        y = float(words[1])
        z = float(words[2])
        print "vertex: ", x, y, z
        #G_table.append([x, y, z, []])
        G_table.append([x, y, z])
        

    # read in the faces
    for i in range(num_faces):
        j = i + num_vertices + 2
        words = lines[j].split()
        nverts = int(words[0])
        if (nverts != 3):
            print "error: this face is not a triangle"
            exit()

        index1 = int(words[1])
        index2 = int(words[2])
        index3 = int(words[3])
        print "triangle: ", index1, index2, index3
        #G_table[index1][3].append(len(V_table))
        V_table.append(index1)
        O_table.append(None)
        #G_table[index2][3].append(len(V_table))
        V_table.append(index2)
        O_table.append(None)
        #G_table[index3][3].append(len(V_table))
        V_table.append(index3)
        O_table.append(None)
        
    calculateOpposites()

# make sure proper error messages get reported when handling key presses
def keyPressed():
    try:
        handleKeyPressed()
    except Exception:
        traceback.print_exc()

def subdivide():
    global G_table, V_table, O_table
    # Create edge table. Indicies are edges. Contains new vertex idx and list containing the two corners opposite of that edge
    edges = []
    # Temporary new V-table
    new_V_table = []
    # For each triangle
    for t in range(0, len(V_table) // 3):
        c = t * 3
        tri_verts = []
        # For each corner, find its opposite, if its edge is not already known
        for i in range(0, 3):
            c = next(c)
            # See if we've already found this corner's edge
            found = False
            for edge in edges:
                if c in edge[1]:
                    tri_verts.append(edge[0])
                    found = True
                    break
            if found:
                continue
            o = opp(c)
            # Find the common edge between the two triangles and drop a new vertex there
            c_verts = [vert(c), vert(next(c)), vert(prev(c))]
            o_verts = [vert(o), vert(next(o)), vert(prev(o))]
            if c_verts[0] not in o_verts:
                v1 = c_verts[1]
                v2 = c_verts[2]
            elif c_verts[1] not in o_verts:
                v1 = c_verts[0]
                v2 = c_verts[2]
            elif c_verts[2] not in o_verts:
                v1 = c_verts[0]
                v2 = c_verts[1]
            else:
                print("SOMETHING VERY BAD HAS HAPPENED!")
            
            edgex = (G_table[v1][0] + G_table[v2][0]) / 2
            edgey = (G_table[v1][1] + G_table[v2][1]) / 2
            edgez = (G_table[v1][2] + G_table[v2][2]) / 2
            edgeidx = len(G_table)
            G_table.append([edgex, edgey, edgez])
            edges.append([edgeidx, [c, o]])
            tri_verts.append(edgeidx)
        # The loop's structure makes c what it was originally and makes tri_verts[0] c.n's edge
        # Build the new triangle from the new verticies
        new_V_table.append(tri_verts[0])
        new_V_table.append(vert(c))
        new_V_table.append(tri_verts[1])
        new_V_table.append(tri_verts[1])
        new_V_table.append(vert(next(c)))
        new_V_table.append(tri_verts[2])
        new_V_table.append(tri_verts[2])
        new_V_table.append(vert(prev(c)))
        new_V_table.append(tri_verts[0])
        new_V_table.append(tri_verts[0])
        new_V_table.append(tri_verts[1])
        new_V_table.append(tri_verts[2])
    # Update V_table
    V_table = new_V_table
    # Update O_table
    calculateOpposites()

def calculateOpposites():
    global V_table, O_table
    O_table = [None] * len(V_table)
    for a in range(0, len(V_table)):
        for b in range(0, len(V_table)):
            if vert(next(a)) == vert(prev(b)) and vert(prev(a)) == vert(next(b)):
                O_table[a] = b
                O_table[b] = a

def inflate():
    global G_table
    for v in G_table:
        n = PVector(v[0], v[1], v[2])
        n.normalize()
        v[0] = n.x
        v[1] = n.y
        v[2] = n.z

def tri(c):
    return c // 3

def vert(c):
    global V_table
    return V_table[c]

def next(c):
    return 3 * tri(c) + (c + 1) % 3

def prev(c):
    return next(next(c))

def opp(c):
    global O_table
    return O_table[c]

def swing(c):
    return next(opp(next(c)))

# process key presses (call your own routines!)
def handleKeyPressed():
    global G_table, V_table, O_table, random_color, random_seed, frame, disp_corner, current_corner
    if key == '1':
        read_mesh ('tetra.ply')
    elif key == '2':
        read_mesh ('octa.ply')
    elif key == '3':
        read_mesh ('icos.ply')
    elif key == '4':
        read_mesh ('star.ply')
    elif key == 'n': # next
        current_corner = next(current_corner)
    elif key == 'p': # previous
        current_corner = prev(current_corner)
    elif key == 'o': # opposite
        current_corner = opp(current_corner)
    elif key == 's': # swing
        current_corner = swing(current_corner)
    elif key == 'd': # subdivide mesh
        subdivide()
    elif key == 'i': # inflate mesh
        inflate()
    elif key == 'r': # toggle random colors
        random_color = not random_color
        random_seed = frame
    elif key == 'c': # toggle showing current corner
        disp_corner = not disp_corner
    elif key == 'q': # quit the program
        exit()

# remember where the user first clicked
def mousePressed():
    global mouseX_old, mouseY_old
    mouseX_old = mouseX
    mouseY_old = mouseY

# change the object rotation matrix while the mouse is being dragged
def mouseDragged():
    global rot_mat
    global mouseX_old, mouseY_old
    
    if (not mousePressed):
        return
    
    dx = mouseX - mouseX_old
    dy = mouseY - mouseY_old
    dy *= -1

    len = sqrt (dx*dx + dy*dy)
    if (len == 0):
        len = 1
    
    dx /= len
    dy /= len
    rmat = PMatrix3D()
    rmat.rotate (len * 0.005, dy, dx, 0)
    rot_mat.preApply (rmat)

    mouseX_old = mouseX
    mouseY_old = mouseY


    
