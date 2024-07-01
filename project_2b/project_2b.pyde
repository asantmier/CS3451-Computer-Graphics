# The object being instanced is the flag

from __future__ import division
import traceback

time = 0   # time is used to move objects from one frame to another

def setup():
    size (800, 800, P3D)
    try:
        frameRate(120)       # this seems to be needed to make sure the scene draws properly
        perspective (60 * PI / 180, 1, 0.1, 1000)  # 60-degree field of view
    except Exception:
        traceback.print_exc()

def draw():
    try:
        global time
        time += 0.01
        
        # set up the lights
        ambientLight(50, 50, 50);
        lightSpecular(255, 255, 255)
        
        # set some of the surface properties
        noStroke()
        specular (180, 180, 180)
        shininess (15.0)
        
        if time <= 3:
            background (200, 200, 255)
            directionalLight (160, 160, 160, -0.3, 0.5, 0.1)
            camera(0, 30, 120, 0, lerp(0, -50, time), 0, 0, 1, 0)
            fill(50, 220, 20)
            pushMatrix()
            translate(0, 50, 0)
            box(400, 1, 400)
            popMatrix()
            pushMatrix()
            translate(0, lerp(0, -50, time), 0)
            rocket()
            popMatrix()
        elif time <= 5:
            background (20, 20, 40)
            directionalLight (160, 70, 60, -0.3, 0.5, 0.1)
            camera(0, lerp(0, -100, time), 150, 0, lerp(0, -100, time), 0, 0, 1, 0)
            pushMatrix()
            translate(0, lerp(0, -100, time), 0)
            rotateY(time)
            rocket()
            popMatrix()
        elif time <= 9:
            background (20, 20, 40)
            directionalLight (160, 70, 60, -0.3, 0.5, 0.1)
            camera(0, lerp(0, -50, time - 5), 150, 0, lerp(0, -50, time - 5), 0, 0, 1, 0)
            pushMatrix()
            translate(0, lerp(0, -50, time - 5), 0)
            stage2()
            popMatrix()
            pushMatrix()
            translate(0, 0, 0)
            rotateZ((time - 5) / 3)
            rotateY(time - 5)
            stage2Drop()
            popMatrix()
        elif time <= 13:
            background (20, 20, 40)
            directionalLight (160, 70, 60, -0.3, 0.5, 0.1)
            camera(0, lerp(0, -50, time - 9), 150, 0, lerp(0, -50, time - 9), 0, 0, 1, 0)
            pushMatrix()
            translate(0, lerp(0, -50, time - 9), 0)
            stage3()
            popMatrix()
            pushMatrix()
            translate(0, 0, 0)
            rotateZ((time - 9) / 4)
            stage3Drop()
            popMatrix()
        elif time <= 18:
            background (20, 20, 40)
            directionalLight (160, 120, 100, -0.3, 0.5, 0.1)
            camera(0, -40, 150, 0, lerp(-50, 0, constrain(time - 13, 0, 1)), 0, 0, 1, 0)
            fill(150, 150, 150)
            pushMatrix()
            translate(0, 200, 0)
            sphere(200)
            popMatrix()
            pushMatrix()
            translate(0, lerp(-50, 0, constrain(time - 13, 0, 1)) + 13, 0)
            stage3()
            popMatrix()
            pushMatrix()
            translate(20, 0, 0)
            flag(255, 0, 0)
            popMatrix()
            pushMatrix()
            translate(-28, 0, 0)
            flag(0, 255, 0)
            popMatrix()
            pushMatrix()
            translate(14, 0, 18)
            flag(0, 0, 255)
            popMatrix()
            pushMatrix()
            translate(-20, 0, 18)
            flag(0, 255, 255)
            popMatrix()
            pushMatrix()
            translate(-20, 0, -18)
            flag(255, 255, 0)
            popMatrix()
            pushMatrix()
            translate(14, 0, -18)
            flag(255, 0, 255)
            popMatrix()

    except Exception:
        traceback.print_exc()
        
def flag(r, g, b):
    fill(255, 255, 255)
    pushMatrix()
    translate(0, -5, 0)
    rotateX(HALF_PI)
    scale(0.5, 0.5, 10)
    cylinder()
    popMatrix()
    
    fill(r, g, b)
    pushMatrix()
    translate(5, -11, 0)
    box(10, 8, 0.5)
    popMatrix()
    
def stage3():
    # Cone
    fill(255, 255, 255)
    pushMatrix()
    translate(0, -30, 0)
    rotateX(-HALF_PI)
    scale(10, 10, 10)
    cone(0.2)
    popMatrix()
    
    # Top stuff (from bottom to top)
    fill(255, 255, 255)
    pushMatrix()
    translate(0, -40, 0)
    rotateX(-HALF_PI)
    scale(2, 2, 3)
    cylinder()
    popMatrix()
    
    fill(255, 255, 255)
    pushMatrix()
    translate(0, -45, 0)
    rotateX(-HALF_PI)
    scale(2, 2, 2)
    cone(0.2)
    popMatrix()
    
    fill(150, 150, 150)
    pushMatrix()
    translate(0, -45, 0)
    rotateX(-HALF_PI)
    scale(.5, .5, 10)
    cylinder()
    popMatrix()
    
    fill(150, 150, 150)
    pushMatrix()
    translate(0, -55.5, 0)
    rotateX(-HALF_PI)
    scale(.5, .5, .5)
    cone(0.2)
    popMatrix()
    
    # Body (from top to bottom)
    fill(0, 0, 0)
    pushMatrix()
    translate(0, -19, 0)
    rotateX(-HALF_PI)
    scale(10, 10, 1)
    cylinder()
    popMatrix()
    
    # Thruster
    fill(50, 50, 50)
    pushMatrix()
    translate(0, -20, 0)
    rotateX(-HALF_PI)
    scale(6, 6, 7)
    cone(0.4)
    popMatrix()
    
def stage3Drop():
    fill(255, 255, 255)
    pushMatrix()
    translate(0, -8, 0)
    rotateX(-HALF_PI)
    scale(10, 10, 10)
    cylinder()
    popMatrix()
    
    fill(0, 0, 0)
    pushMatrix()
    translate(0, 3, 0)
    rotateX(-HALF_PI)
    scale(10, 10, 1)
    cylinder()
    popMatrix()
    
    # Thruster
    fill(50, 50, 50)
    pushMatrix()
    translate(0, 4, 0)
    rotateX(-HALF_PI)
    scale(6, 6, 7)
    cone(0.4)
    popMatrix()

def stage2():
    # Cone
    fill(255, 255, 255)
    pushMatrix()
    translate(0, -30, 0)
    rotateX(-HALF_PI)
    scale(10, 10, 10)
    cone(0.2)
    popMatrix()
    
    # Top stuff (from bottom to top)
    fill(255, 255, 255)
    pushMatrix()
    translate(0, -40, 0)
    rotateX(-HALF_PI)
    scale(2, 2, 3)
    cylinder()
    popMatrix()
    
    fill(255, 255, 255)
    pushMatrix()
    translate(0, -45, 0)
    rotateX(-HALF_PI)
    scale(2, 2, 2)
    cone(0.2)
    popMatrix()
    
    fill(150, 150, 150)
    pushMatrix()
    translate(0, -45, 0)
    rotateX(-HALF_PI)
    scale(.5, .5, 10)
    cylinder()
    popMatrix()
    
    fill(150, 150, 150)
    pushMatrix()
    translate(0, -55.5, 0)
    rotateX(-HALF_PI)
    scale(.5, .5, .5)
    cone(0.2)
    popMatrix()
    
    # Body (from top to bottom)
    fill(0, 0, 0)
    pushMatrix()
    translate(0, -19, 0)
    rotateX(-HALF_PI)
    scale(10, 10, 1)
    cylinder()
    popMatrix()
    
    fill(255, 255, 255)
    pushMatrix()
    translate(0, -8, 0)
    rotateX(-HALF_PI)
    scale(10, 10, 10)
    cylinder()
    popMatrix()
    
    fill(0, 0, 0)
    pushMatrix()
    translate(0, 3, 0)
    rotateX(-HALF_PI)
    scale(10, 10, 1)
    cylinder()
    popMatrix()
    
    # Thruster
    fill(50, 50, 50)
    pushMatrix()
    translate(0, 4, 0)
    rotateX(-HALF_PI)
    scale(6, 6, 7)
    cone(0.4)
    popMatrix()

def stage2Drop():
    fill(255, 255, 255)
    pushMatrix()
    translate(0, 22, 0)
    rotateX(-HALF_PI)
    scale(10, 10, 18)
    cylinder()
    popMatrix()
    
    # Thrusters
    fill(50, 50, 50)
    pushMatrix()
    translate(0, 42, 0)
    rotateX(-HALF_PI)
    scale(5, 5, 7)
    cone(0.4)
    popMatrix()
    
    # Symmetrically place smaller thrusters
    pushMatrix()
    for theta in range(4):
        thruster()
        rotateY(HALF_PI)
    popMatrix()

def rocket():
    # Cone
    fill(255, 255, 255)
    pushMatrix()
    translate(0, -30, 0)
    rotateX(-HALF_PI)
    scale(10, 10, 10)
    cone(0.2)
    popMatrix()
    
    # Top stuff (from bottom to top)
    fill(255, 255, 255)
    pushMatrix()
    translate(0, -40, 0)
    rotateX(-HALF_PI)
    scale(2, 2, 3)
    cylinder()
    popMatrix()
    
    fill(255, 255, 255)
    pushMatrix()
    translate(0, -45, 0)
    rotateX(-HALF_PI)
    scale(2, 2, 2)
    cone(0.2)
    popMatrix()
    
    fill(150, 150, 150)
    pushMatrix()
    translate(0, -45, 0)
    rotateX(-HALF_PI)
    scale(.5, .5, 10)
    cylinder()
    popMatrix()
    
    fill(150, 150, 150)
    pushMatrix()
    translate(0, -55.5, 0)
    rotateX(-HALF_PI)
    scale(.5, .5, .5)
    cone(0.2)
    popMatrix()
    
    # Body (from top to bottom)
    fill(0, 0, 0)
    pushMatrix()
    translate(0, -19, 0)
    rotateX(-HALF_PI)
    scale(10, 10, 1)
    cylinder()
    popMatrix()
    
    fill(255, 255, 255)
    pushMatrix()
    translate(0, -8, 0)
    rotateX(-HALF_PI)
    scale(10, 10, 10)
    cylinder()
    popMatrix()
    
    fill(0, 0, 0)
    pushMatrix()
    translate(0, 3, 0)
    rotateX(-HALF_PI)
    scale(10, 10, 1)
    cylinder()
    popMatrix()
    
    fill(255, 255, 255)
    pushMatrix()
    translate(0, 22, 0)
    rotateX(-HALF_PI)
    scale(10, 10, 18)
    cylinder()
    popMatrix()
    
    # Thrusters
    fill(50, 50, 50)
    pushMatrix()
    translate(0, 42, 0)
    rotateX(-HALF_PI)
    scale(5, 5, 7)
    cone(0.4)
    popMatrix()
    
    # Symmetrically place smaller thrusters
    pushMatrix()
    for theta in range(4):
        thruster()
        rotateY(HALF_PI)
    popMatrix()

# Helper method for making thrusters
def thruster():
    fill(255, 255, 255)
    pushMatrix()
    translate(6, 35, 6)
    rotateX(-HALF_PI)
    scale(4, 4, 5)
    cone(0.4)
    popMatrix()
    
    fill(100, 100, 100)
    pushMatrix()
    translate(6, 41, 6)
    rotateX(-HALF_PI)
    scale(3, 3, 5)
    cone(0.4)
    popMatrix()
    
    fill(255, 255, 255)
    pushMatrix()
    translate(7, 35, 7)
    rotateY(-QUARTER_PI)
    scale(4, 4, 5)
    box(2, 2, .1)
    popMatrix()
    
    fill(255, 255, 255)
    pushMatrix()
    translate(6, 32, 6)
    rotateY(-QUARTER_PI)
    rotateZ(radians(35))
    scale(4, 3.85, 5)
    box(2, 2, .1)
    popMatrix()

# cylinder with radius = 1, z range in [-1,1]
def cylinder(sides = 50):
    # first endcap
    beginShape()
    for i in range(sides):
        theta = i * 2 * PI / sides
        x = cos(theta)
        y = sin(theta)
        vertex ( x,  y, -1)
    endShape(CLOSE)
    # second endcap
    beginShape()
    for i in range(sides):
        theta = i * 2 * PI / sides
        x = cos(theta)
        y = sin(theta)
        vertex ( x,  y, 1)
    endShape(CLOSE)
    # round main body
    x1 = 1
    y1 = 0
    for i in range(sides):
        theta = (i + 1) * 2 * PI / sides
        x2 = cos(theta)
        y2 = sin(theta)
        beginShape()
        normal (x1, y1, 0)
        vertex (x1, y1, 1)
        vertex (x1, y1, -1)
        normal (x2, y2, 0)
        vertex (x2, y2, -1)
        vertex (x2, y2, 1)
        endShape(CLOSE)
        x1 = x2
        y1 = y2
        
# cone made by shrinking one cap of a cylinder
def cone(scal, sides = 50):
    # first endcap
    beginShape()
    for i in range(sides):
        theta = i * 2 * PI / sides
        x = cos(theta) * scal
        y = sin(theta) * scal
        vertex ( x,  y, -1)
    endShape(CLOSE)
    # second endcap
    beginShape()
    for i in range(sides):
        theta = i * 2 * PI / sides
        x = cos(theta)
        y = sin(theta)
        vertex ( x,  y, 1)
    endShape(CLOSE)
    # round main body
    x1 = 1
    y1 = 0
    for i in range(sides):
        theta = (i + 1) * 2 * PI / sides
        x2 = cos(theta)
        y2 = sin(theta)
        beginShape()
        normal (x1, y1, 0)
        vertex (x1, y1, 1)
        vertex (x1 * scal, y1 * scal, -1)
        normal (x2, y2, 0)
        vertex (x2 * scal, y2 * scal, -1)
        vertex (x2, y2, 1)
        endShape(CLOSE)
        x1 = x2
        y1 = y2
