red =     0xffff0000
yellow =  0xffffff00
green =   0xff00ff00
cyan =    0xff00ffff
blue =    0xff0000ff
magenta = 0xffff00ff

# this is 1 less than the number of child satellites the main square will have
recursionDepth = 4
# how many satellites each square should have
numSatellites = 4

def setup():
    size(600, 600)

def draw():
    # clear screen
    background(123, 123, 123)
    noStroke()
    # calculate scale
    scale = 1 - (float(mouseY) / height)
    # calculate mouse position relative to center of the screen
    relMouseX = mouseX - (width / 2)
    
    size = width / 3
    hsize = size / 2
    x = width / 2
    y = height / 2
    
    satellite(x, y, size, hsize, scale, recursionDepth, relMouseX)
    
# create satellites around square at (x, y) of size where hsize is half the size to save
# some math, scale is the scale of the pattern, and children is the depth of recursion
# and relMouseX is the scaled mouse position the rect DIRECTLY created in this function
# will use
def satellite(x, y, size, hsize, scale, children, relMouseX):
    findFill(children)
    rect(x - hsize, y - hsize, size, size)
    if children == 0:
        return
    
    sizep = size * scale
    hsizep = sizep / 2
    # locate center of satellite A
    xp = x - hsizep
    yp = y - hsize - hsizep
    # offset based on mouse cursor
    xp += relMouseX + hsizep # +hsizep makes mouse control the center
    relMouseX *= scale # scale mouse position for next layer of satellites
    for i in range(numSatellites):
        satellite(xp, yp, sizep, hsizep, scale, children - 1, relMouseX)
        xp, yp = rot(xp, yp, x, y)
    
# changes fill color based on recursion depth
def findFill(depth):
    depth %= 6 # allows for infinite depth by looping colors
    if depth == 5:
        fill(red)
    elif depth == 4:
        fill(yellow)
    elif depth == 3:
        fill(green)
    elif depth == 2:
        fill(cyan)
    elif depth == 1:
        fill(blue)
    elif depth == 0:
        fill(magenta)

# rotates (x, y) around (xc, yc) by 90 degrees counterclockwise
def rot(x, y, xc, yc):
    xt = x - xc
    yt = -(y - yc)
    xr = -yt
    yr = xt
    x2 = xr + xc
    y2 = yc - yr
    return (x2, y2)
