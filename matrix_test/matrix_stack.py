# Your Matrix Stack Library

# you should modify the provided empty routines to complete the assignment

identity = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
matrix_stack = ["a", "b", "c"]

def multiply(a, b):
    c = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(4):
        for j in range(4):
            product = 0
            for k in range(4):
                product += a[i][k] * b[k][j]
            c[i][j] = product
    return c

def gtInitialize():
    global matrix_stack
    matrix_stack = []
    matrix_stack.append(identity)

def gtPopMatrix():
    global matrix_stack
    if len(matrix_stack) == 1:
        print("Matrix stack only has one element")
    else:
        matrix_stack.pop(-1)

def gtPushMatrix():
    global matrix_stack
    matrix_stack.append(matrix_stack[-1])

def gtScale(x,y,z):
    global matrix_stack
    scal = [[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]]
    matrix_stack[-1] = multiply(matrix_stack[-1], scal)

def gtTranslate(x,y,z):
    global matrix_stack
    trans = [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]
    matrix_stack[-1] = multiply(matrix_stack[-1], trans)

def gtRotateX(theta):
    global matrix_stack
    theta = radians(theta)
    rot = [[1, 0, 0, 0], [0, cos(theta), -sin(theta), 0], [0, sin(theta), cos(theta), 0], [0, 0, 0, 1]]
    matrix_stack[-1] = multiply(matrix_stack[-1], rot)

def gtRotateY(theta):
    global matrix_stack
    theta = radians(theta)
    rot = [[cos(theta), 0, sin(theta), 0], [0, 1, 0, 0], [-sin(theta), 0, cos(theta), 0], [0, 0, 0, 1]]
    matrix_stack[-1] = multiply(matrix_stack[-1], rot)

def gtRotateZ(theta):
    global matrix_stack
    theta = radians(theta)
    rot = [[cos(theta), -sin(theta), 0, 0], [sin(theta), cos(theta), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    matrix_stack[-1] = multiply(matrix_stack[-1], rot)

def print_ctm():
    global matrix_stack
    print(matrix_stack[-1][0])
    print(matrix_stack[-1][1])
    print(matrix_stack[-1][2])
    print(matrix_stack[-1][3])
    print
