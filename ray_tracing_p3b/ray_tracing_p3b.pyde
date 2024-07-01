# This is the provided code for the ray tracing project.
#
# The most important part of this code is the command interpreter, which
# parses the scene description (.cli) files.
# Name: Allen Santmier

from __future__ import division
import traceback
from sphere import Sphere
from triangle import Triangle
from camera import Camera
from light import Light
from material import Material
from ray import Ray
import time
from fastpvector import PVector

TIMING = True        # If true, timing behavior will be enabled. This is for DEVELOPMENT ONLY!
TIMING_CYCLES = 1    # Number of cycles to average timing over
INFO_ONLY = False      # If true, the scene will not be rendered and only info read from the CLI file will be printed

debug_flag = False   # print debug information when this is True

epsilon = 0.0005       # Offset along shadow vector to avoid intersecting the same face we're shading
num_refl = 10      # Number of reflections to do

# Some globals
objects = []
bgColor = (0, 0, 0)
cam = Camera()
lightSources = []

def setup():
    size(320, 320) 
    noStroke()
    colorMode(RGB, 1.0)  # Processing color values will be in [0, 1]  (not 255)
    background(0, 0, 0)
    frameRate(30)

# make sure proper error messages get reported when handling key presses
def keyPressed():
    try:
        # If TIMING is set to True, some extra structure is added to find the average runtime of the ray tracing algorithm
        if TIMING:
            print("WARNING: TIMING ENABLED! TURN IT OFF BEFORE SUBMITTING!")
            total = 0
            n = TIMING_CYCLES
            for _ in range(n):
                t0 = time.time()
                handleKeyPressed()
                t1 = time.time()
                total += t1 - t0
            print("Average time elapsed: {}s.".format(total / n))
        else:
            handleKeyPressed()
    except Exception:
        traceback.print_exc()

# read and interpret a scene description .cli file based on which key has been pressed
def handleKeyPressed():
    if key == '1':
        interpreter("01_one_sphere.cli")
    elif key == '2':
        interpreter("02_three_spheres.cli")
    elif key == '3':
        interpreter("03_shiny_sphere.cli")
    elif key == '4':
        interpreter("04_many_spheres.cli")
    elif key == '5':
        interpreter("05_one_triangle.cli")
    elif key == '6':
        interpreter("06_icosahedron_and_sphere.cli")
    elif key == '7':
        interpreter("07_colorful_lights.cli")
    elif key == '8':
        interpreter("08_reflective_sphere.cli")
    elif key == '9':
        interpreter("09_mirror_spheres.cli")
    elif key == '0':
        interpreter("10_reflections_in_reflections.cli")
    elif key == '-':
        interpreter("11_star.cli")

# You should add code for each command that calls routines that you write.
# Some of the commands will not be used until Part B of this project.
def interpreter(fname):
    global objects, bgColor, cam, lightSources
    
    reset_scene()  # you should initialize any data structures that you will use here
    
    fname = "data/" + fname
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()

    lastMaterial = None
    vertexBuffer = []

    # parse the lines in the file in turn
    for line in lines:
        words = line.split()  # split up the line into individual tokens
        if len(words) == 0:   # skip empty lines
            continue
        if words[0] == 'sphere':
            x = float(words[2])
            y = float(words[3])
            z = float(words[4])
            radius = float(words[1])
            objects.append(Sphere(x, y, z, radius, lastMaterial)) # uses the last defined material
        elif words[0] == 'fov':
            fov = float(words[1])
            cam.fov = fov
        elif words[0] == 'eye':
            ex = float(words[1])
            ey = float(words[2])
            ez = float(words[3])
            cam.set_eye(ex, ey, ez)
        elif words[0] == 'uvw':
            ux = float(words[1])
            uy = float(words[2])
            uz = float(words[3])
            vx = float(words[4])
            vy = float(words[5])
            vz = float(words[6])
            wx = float(words[7])
            wy = float(words[8])
            wz = float(words[9])
            cam.set_frame(ux, uy, uz, vx, vy, vz, wx, wy, wz)
        elif words[0] == 'background':
            r = float(words[1])
            g = float(words[2])
            b = float(words[3])
            bgColor = (r, g, b)
        elif words[0] == 'light':
            x = float(words[1])
            y = float(words[2])
            z = float(words[3])
            r = float(words[4])
            g = float(words[5])
            b = float(words[6])
            lightSources.append(Light(x, y, z, r, g, b))
        elif words[0] == 'surface':
            dr = float(words[1])
            dg = float(words[2])
            db = float(words[3])
            ar = float(words[4])
            ag = float(words[5])
            ab = float(words[6])
            sr = float(words[7])
            sg = float(words[8])
            sb = float(words[9])
            spec_power = float(words[10])
            k_refl = float(words[11])
            lastMaterial = Material(dr, dg, db, ar, ag, ab, sr, sg, sb, spec_power, k_refl)
        elif words[0] == 'begin':
            vertexBuffer = []
        elif words[0] == 'vertex':
            x = float(words[1])
            y = float(words[2])
            z = float(words[3])
            vertexBuffer.append(PVector(x, y, z))
        elif words[0] == 'end':
            objects.append(Triangle(vertexBuffer[0], vertexBuffer[1], vertexBuffer[2], lastMaterial))
        elif words[0] == 'render':
            render_scene()    # render the scene (this is where most of the work happens)
        elif words[0] == '#':
            pass  # ignore lines that start with the comment symbol (pound-sign)
        else:
            print ("unknown command: " + word[0])

# render the ray tracing scene
def render_scene():
    global debug_flag, objects, bgColor, cam, lightSources
    # Some info about the scene
    print("Background color: {}".format(bgColor))
    print("Eye : {}, FOV: {}, U {} V {} W {}".format(cam.eye, cam.fov, cam.u, cam.v, cam.w))
    print("Objects: {}".format(objects))
    print("Lights: {}".format(lightSources))
    # Scene info only debugging
    if INFO_ONLY: return
    # Timing
    t0 = time.time()
    progress_freq = 0
    tl = t0
    # d is constant throughout
    d = 1 / tan(radians(cam.fov / 2))
    for j in range(height):
        for i in range(width):
            # Maybe set a debug flag to true for ONE pixel.
            # Have routines (like ray/sphere intersection)print extra information if this flag is set.
            debug_flag = False
            if i == 211 and j == 96:
                debug_flag = True
            
            # Progress
            t1 = time.time()
            progress_freq += t1 - tl
            if progress_freq >= 5:
                progress_freq -= 5
                print("{}/{} pixels done. {}% complete".format((j * width) + i, height * width, (((j * width) + i) / (height * width)) * 100))
            tl = t1
            
            # Find direction of ray
            u = -1 + ((2 * i) / width)
            v = -1 + ((2 * (height - j)) / height)
            dir = (-d * cam.w + u * cam.u + v * cam.v).normalize()
            
            ray = Ray(cam.eye, dir)
            
            r, g, b = raycast(ray, 0)
            
            pix_color = color(r, g, b)
            set (i, j, pix_color)         # draw the pixel with the calculated color
    print("Scene render complete")
    # Timing
    t1 = time.time()
    if TIMING:
        print("Time elapsed: {}s.".format(t1 - t0))

# Generic raycast coloring
def raycast(ray, refl_depth):
    global debug_flag, objects, bgColor, cam, lightSources
    # set default color to background
    r = bgColor[0]
    g = bgColor[1]
    b = bgColor[2]
    t = None
    closest_obj = None
    # Ray intersection
    for object in objects:
        if isinstance(object, Sphere):
            solution = intersect_sphere(ray, object) # Sphere intersection
        else: # no need to compare, we only process two types of objects
            solution = intersect_tri(ray, object) # Triangle intersection
        
        # Find closest object
        if solution and (t == None or solution < t):
            t = solution
            closest_obj = object
    if t:
        hit = ray.evaluate(t)
        if isinstance(closest_obj, Sphere):
            N = (hit - closest_obj.center).normalize()
        else:
            N = closest_obj.normal
            # Make sure the normal is facing the right way
            if PVector.dot(ray.direction, N) > 0:
                N = -1 * N
        V = (cam.eye - hit).normalize()
        # Ambient contribution
        r = closest_obj.material.ambientColor[0]
        g = closest_obj.material.ambientColor[1]
        b = closest_obj.material.ambientColor[2]
        # Light contribution
        for light in lightSources:
            L = (light.pos - hit).normalize()
            
            # Check if in shadow
            shadow_ray = Ray(hit, L)
            if debug_flag:
                print("Hit: {}, Shadow {}. Light at {}".format(hit, shadow_ray, light.pos))
            in_shadow = False
            # CHECK IF DISTANCE OF HIT OBJECT IS CLOSER THAN THE LIGHT!
            light_dist = PVector.mag(hit - light.pos)
            for object in objects:
                # it is not self intersecting
                if isinstance(object, Sphere):
                    shadow_caster = intersect_sphere(shadow_ray, object)
                else: 
                    shadow_caster = intersect_tri(shadow_ray, object)
                if shadow_caster != None:
                    dist = PVector.mag(hit - shadow_ray.evaluate(shadow_caster))
                    if dist < light_dist:
                        in_shadow = True
                        break
            if debug_flag:
                print("Shadow {} at t={}".format(in_shadow, shadow_caster))
            if in_shadow:
                continue
            
            # Caulculate color under this light
            diffuseContribution = max(0, PVector.dot(N, L))
            H = (V + L).normalize()
            specularContribution = pow(max(0, PVector.dot(N, H)), closest_obj.material.specularPower)
            r += light.color[0] * ((closest_obj.material.diffuseColor[0] * diffuseContribution) + (closest_obj.material.specularColor[0] * specularContribution))
            g += light.color[1] * ((closest_obj.material.diffuseColor[1] * diffuseContribution) + (closest_obj.material.specularColor[1] * specularContribution))
            b += light.color[2] * ((closest_obj.material.diffuseColor[2] * diffuseContribution) + (closest_obj.material.specularColor[2] * specularContribution))
        # Ideal specular reflection
        if closest_obj.material.k_refl > 0 and refl_depth < num_refl:
            # we use ray.direction because we care about the view of the ray caster for each recursion of this function
            R = (ray.direction + (2 * PVector.dot(N, -1 * ray.direction)) * N).normalize()
            refl_ray = Ray(hit, R)
            # Recursive raycasting
            r_r, r_g, r_b = raycast(refl_ray, refl_depth + 1)
            r += closest_obj.material.k_refl * r_r
            g += closest_obj.material.k_refl * r_g
            b += closest_obj.material.k_refl * r_b
            if debug_flag:
                print("Ray #{}. r{}, g{}, b{}".format(refl_depth, r, g, b))
    return r, g, b

# Returns nearest t to camera. Automatically handles self intersection
def intersect_tri(ray, tri):
    den = PVector.dot(tri.normal, ray.direction)
    # no intersection if ray is in plane
    if den == 0:
        return None
    d = tri.normal.x * tri.v1.x + tri.normal.y * tri.v1.y + tri.normal.z * tri.v1.z
    num = -(tri.normal.x * ray.origin.x + tri.normal.y * ray.origin.y + tri.normal.z * ray.origin.z - d)
    t = num / den
    # Only return nonnegative t
    if t >= 0 and t >= epsilon:
        hit = ray.evaluate(t)
        if tri.half_plane_test(hit):
            return t
    return None

# Returns nearest t to camera. Automatically handles self intersection
def intersect_sphere(ray, sphere):
    a = PVector.dot(ray.direction, ray.direction)
    emc = ray.origin - sphere.center # this might be faster?
    b = PVector.dot(ray.direction, emc)
    c = PVector.dot(emc, emc) - sq(sphere.radius)
    discrim = sq(b) - (a * c)
    if discrim < 0:
        # no hit
        return None
    elif discrim == 0:
        # one solution
        t = -b / a
        # only return nonnegative values
        if t >= 0 and t >= epsilon:
            return t
        else:
            return None
    else:
        # two solutions
        sqrtdiscrim = sqrt(discrim)
        t1 = (-b + sqrtdiscrim) / a
        t2 = (-b - sqrtdiscrim) / a
        # only return nonnegative values
        if (t1 >= 0 and t2 >= 0) and (t1 >= epsilon and t2 >= epsilon):
            return min(t1, t2)
        elif t1 >= 0 and t2 < 0 and t1 >= epsilon:
            return t1
        elif t1 < 0 and t2 >= 0 and t2 >= epsilon:
            return t2
        else:
            return None

# here you should reset any data structures that you will use for your scene (e.g. list of spheres)
def reset_scene():
    global objects, bgColor, cam, lightSources
    objects = []
    bgColor = (0, 0, 0)
    cam = Camera()
    lightSources = []

# prints mouse location clicks, for help debugging
def mousePressed():
    print ("You pressed the mouse at " + str(mouseX) + " " + str(mouseY))

# this function should remain empty for this assignment
def draw():
    pass
