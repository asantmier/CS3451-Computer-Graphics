# This is the provided code for the ray tracing project.
#
# The most important part of this code is the command interpreter, which
# parses the scene description (.cli) files.

from __future__ import division
import traceback
from sphere import Sphere
from camera import Camera
from light import Light
from material import Material
from ray import Ray
import time

TIMING = False        # If true, timing behavior will be enabled. This is for DEVELOPMENT ONLY!

debug_flag = False   # print debug information when this is True

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
            global t_shading_time, t_intersecting_time
            total = 0
            t_shading_time = 0
            t_intersecting_time = 0
            n = 10
            for _ in range(n):
                t0 = time.time()
                handleKeyPressed()
                t1 = time.time()
                total += t1 - t0
            print("Average time elapsed: {}\nShading: {}\tIntersecting: {}".format(total / n, t_shading_time / n, t_intersecting_time / n))
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
            lastMaterial = Material(dr, dg, db)
        elif words[0] == 'begin':
            pass
        elif words[0] == 'vertex':
            pass
        elif words[0] == 'end':
            pass
        elif words[0] == 'render':
            render_scene()    # render the scene (this is where most of the work happens)
        elif words[0] == '#':
            pass  # ignore lines that start with the comment symbol (pound-sign)
        else:
            print ("unknown command: " + word[0])

# render the ray tracing scene
def render_scene():
    global debug_flag, objects, bgColor, cam, lightSources
    global t_shading_time, t_intersecting_time
    # Some info about the scene
    print("Background color: {}".format(bgColor))
    print("Eye : {}, FOV: {}, U {} V {} W {}".format(cam.eye, cam.fov, cam.u, cam.v, cam.w))
    print("Objects: {}".format(objects))
    print("Lights: {}".format(lightSources))
    # Timing
    t0 = time.time()
    shading_time = 0
    intersecting_time = 0
    # d is constant throughout
    d = 1 / tan(radians(cam.fov / 2))
    for j in range(height):
        for i in range(width):
            # Maybe set a debug flag to true for ONE pixel.
            # Have routines (like ray/sphere intersection)print extra information if this flag is set.
            debug_flag = False
            if i == 195 and j == 131:
                debug_flag = True
            
            # Find direction of ray
            u = -1 + ((2 * i) / width)
            v = -1 + ((2 * (height - j)) / height)
            dir = (-d * cam.w + u * cam.u + v * cam.v).normalize()
            
            ray = Ray(cam.eye, dir)
            # set default color to background
            pix_color = color(bgColor[0], bgColor[1], bgColor[2])
            
            t = None
            closest_obj = None
            for object in objects:
                # Timing
                t1 = time.time()
                shading_time += t1 - t0
                s0 = time.time()
                
                solution = intersect_sphere(ray, object) # Sphere intersection
                
                s1 = time.time()
                intersecting_time += s1 - s0
                t0 = time.time()
                # Find closest object
                if solution and (t == None or solution < t):
                    t = solution
                    closest_obj = object
            if t:
                hit = ray.evaluate(t)
                N = (hit - closest_obj.center).normalize()
                r = 0
                g = 0
                b = 0
                for light in lightSources:
                    L = (light.pos - hit).normalize()
                    diffuseContribution = max(0, N.dot(L))
                    r += light.color[0] * (closest_obj.material.diffuseColor[0] * diffuseContribution)
                    g += light.color[1] * (closest_obj.material.diffuseColor[1] * diffuseContribution)
                    b += light.color[2] * (closest_obj.material.diffuseColor[2] * diffuseContribution)
                # Averages color components for multiple lights
                pix_color = color(r / len(lightSources), g / len(lightSources), b / len(lightSources))
            set (i, j, pix_color)         # draw the pixel with the calculated color
    # Timing
    t1 = time.time()
    shading_time += t1 - t0
    print("Time elapsed: {}s. {}s shading, {}s intersecting".format(shading_time + intersecting_time, shading_time, intersecting_time))
    if TIMING:
        t_shading_time += shading_time
        t_intersecting_time += intersecting_time

# Returns nearest t to camera
def intersect_sphere(ray, sphere):
    a = ray.direction.dot(ray.direction)
    emc = ray.origin - sphere.center # this might be faster?
    b = ray.direction.dot(emc)
    c = emc.dot(emc) - sq(sphere.radius)
    discrim = sq(b) - (a * c)
    if discrim < 0:
        # no hit
        return None
    elif discrim == 0:
        # one solution
        t = -b / a
        return t
    else:
        # two solutions
        sqrtdiscrim = sqrt(discrim)
        t1 = (-b + sqrtdiscrim) / a
        t2 = (-b - sqrtdiscrim) / a
        return min(t1, t2)

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
