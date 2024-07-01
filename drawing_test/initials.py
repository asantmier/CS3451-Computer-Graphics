# The routine below should draw your initials in perspective

from matrix_stack import *
from drawlib import *

def persp_initials():
    gtInitialize()
    gtPerspective (60, -100, 100)
    gtPushMatrix()
    gtTranslate(-4, -4, -10)
    gtRotateY(60)
    
    gtBeginShape()
    #A
    gtVertex(0, 0, 0)
    gtVertex(1, 4, 0)
    
    gtVertex(1, 4, 0)
    gtVertex(2, 8, 0)
    
    gtVertex(2, 8, 0)
    gtVertex(3, 4, 0)
    
    gtVertex(3, 4, 0)
    gtVertex(4, 0, 0)
    
    gtVertex(1, 4, 0)
    gtVertex(3, 4, 0)
    #S
    gtVertex(4, 0, 0)
    gtVertex(8, 0, 0)
    
    gtVertex(8, 0, 0)
    gtVertex(8, 4, 0)
    
    gtVertex(8, 4, 0)
    gtVertex(4, 4, 0)
    
    gtVertex(4, 4, 0)
    gtVertex(4, 8, 0)
    
    gtVertex(4, 8, 0)
    gtVertex(8, 8, 0)
    
    gtEndShape()
    
    gtPopMatrix()
