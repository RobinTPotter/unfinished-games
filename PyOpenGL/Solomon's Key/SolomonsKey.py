

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

name = "solomon\'s key"

class Baddie:
    def __init__(self,type):
        pass



def DrawSolomon():
    glTranslate(1,-0.15,0)
    glTranslate(4,2,0)
    glRotatef(-90.0,1.0,0,0)
    glScale(0.25,0.25,0.25)

    
    #hat
    glPushMatrix()
    glTranslate(0,0,0.5)
    glutSolidCone(1,2,12,6)
    glPopMatrix()
    
    #head/body
    glPushMatrix()
    glTranslate(0,0,0)
    glutSolidSphere(1,12,12)            
    glPopMatrix()
    
    #left arm
    glPushMatrix()
    glTranslate(0,0.9,0)
    glutSolidSphere(0.5,12,12)            
    glPopMatrix()
    
    #right arm
    glPushMatrix()
    glTranslate(0,-0.9,0)
    glutSolidSphere(0.5,12,12)            
    glPopMatrix()
    
    #left foot
    glPushMatrix()
    glTranslate(0,0.75,-1)
    glScale(2,1,1)
    glutSolidSphere(0.5,12,12)            
    glPopMatrix()
    
    #right foot
    glPushMatrix()
    glTranslate(0,-0.75,-1)
    glScale(2,1,1)
    glutSolidSphere(0.5,12,12)            
    glPopMatrix()
    

class Level:
    grid=None
    baddies=[]
    
    def __init__(self,griddata):
        griddata.reverse()
        self.grid=griddata

    def draw(self):
        rr=0
        for r in self.grid:
            cc=0
            for c in r:
                cc+=1
                glPushMatrix()
                glTranslate(cc,rr,0)
                if c in ["b","s"]: 
                    if c=="b": color = [0.5,0.5,1.0,1.0]
                    elif c=="s": color = [1.0,1.0,0.0,1.0]
                    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
                    glutSolidCube(1)
                glPopMatrix()
                
            rr+=1
                

class SolomonsKey:

    level=None
    keys={}
    xx,yy,zz=5.5,4.0,12.0

    def __init__(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(640,480)
        glutCreateWindow(name)

        glClearColor(0.,0.,0.,1.)
        glShadeModel(GL_FLAT)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        lightZeroPosition = [10.,4.,10.,1.]
        lightZeroColor = [0.8,1.0,0.8,1.0] #green tinged
        glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
        glEnable(GL_LIGHT0)
        glutSpecialFunc(self.keydownevent)
        glutSpecialUpFunc(self.keyupevent)

        glutKeyboardFunc(self.keydownevent)
        glutKeyboardUpFunc(self.keyupevent)
        glutDisplayFunc(self.display)
        glutIdleFunc(self.display)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(60.0,640.0/480.,1.,50.)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        self.level=Level([
            "b.............b",
            ".......d.......",
            ".5.............",
            ".....sbbbs.....",
            ".....b343b.....",
            "..g..sbbbs..g..",
            "......bbb......",
            "...2.......2...",
            "...sbs.1.sbs...",
            "...b@bbbbbkb...",
            "...sbs...sbs...",
            "b.............b"])

        glutMainLoop()

        return

    def display(self):

        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #print (self.xx,self.yy,self.zz)
        gluLookAt(self.xx,self.yy,self.zz,
                  5.5,4.0,0.0,
                  0,1,0)
        glPushMatrix()
        #color = [1.0,0.,0.,1.]
        #glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
        #glutSolidSphere(2,20,20)
        self.level.draw()
        glPopMatrix()
        DrawSolomon()
        try:
            if self.keys["x"]: self.xx+=0.1
            if self.keys["z"]: self.xx-=0.1
            if self.keys["d"]: self.yy+=0.1
            if self.keys["c"]: self.yy-=0.1
            if self.keys["f"]: self.zz+=0.1
            if self.keys["v"]: self.zz-=0.1
        except:
            pass    

        #print "."
        glutSwapBuffers()
        #return

    def keydownevent(self,c,x,y):
        #print (c,x,y)
        self.keys[c]=True

    def keyupevent(self,c,x,y):
        #print (c,x,y)
        if self.keys.has_key(c): self.keys[c]=False


if __name__ == '__main__': SolomonsKey()
