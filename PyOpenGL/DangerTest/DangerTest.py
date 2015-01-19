from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import random 
import sys
from time import time
#import math

name = "thing"

colours={}
colours["red"]=[1.0,0.0,0.0,1.0]
colours["green"]=[0.0,1.0,0.0,1.0]
colours["blue"]=[0.0,0.0,1.0,1.0]
colours["yellow"]=[1.0,1.0,0.0,1.0]
colours["cyan"]=[0.0,1.0,1.0,1.0]
colours["pink"]=[1.0,0.0,1.0,1.0]
colours["white"]=[1.0,1.0,1.0,1.0]
  
class Thing:

    lastFrameTime=0
    
    xx,yy,zz=0,0,10
    cxx,cyy,czz=0,0,0
    X=0
    
    xRot=0
    yRot=0
    mPos=[0,0]
    speed=0.1

    def animate(self,FPS=1):
        
        currentTime=time()         
        
        
        self.X+=1
        if self.X>1000: self.X=0
               
        print "posting redisplay"
        glutPostRedisplay()    
        
        tt=int(1000/FPS)
        print tt, FPS
        glutTimerFunc(tt, self.animate, FPS)
        drawTime=currentTime-self.lastFrameTime
        self.topFPS=int(1000/drawTime)
        if int(100*time())%100==0: print "draw time "+str(drawTime)+" top FPS "+str(1000/drawTime)
        
    def draw(self):
            
	glTranslate(0,0,8)
	glRotate(-self.yRot,1,0,0)
	glRotate(-self.xRot,0,1,0)
	    
	    
        f=open("DangerCode.txt","r")
        code=f.read()
        print "DC:"+code
        exec(code)

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
        glutMotionFunc(self.mousedrag)
        glutMouseFunc(self.mouse)
        '''
        glutSpecialFunc(self.keydownevent)
        glutSpecialUpFunc(self.keyupevent)
        glutKeyboardFunc(self.keydownevent)
        glutKeyboardUpFunc(self.keyupevent)
        '''
        
        glutDisplayFunc(self.display)
        #glutIdleFunc(self.display)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(60.0,640.0/480.,1.,50.)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        
        self.animate(FPS=15)
        
        glutMainLoop()
        
        
        return

    def mousedrag(self,x,y):
	print ((x,y))
	self.xRot+=(self.mPos[0]-x)*self.speed
	self.yRot+=(self.mPos[1]-y)*self.speed
	self.mPos=[x,y]
	
	
    def mouse(self,button,state,x,y):
	print ((button,state,x,y))
	self.mPos=[x,y]

    def display(self):

        glEnable (GL_BLEND)
        glEnable (GL_POLYGON_SMOOTH)
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #print (self.xx,self.yy,self.zz)                 
        
        gluLookAt(self.xx,self.yy,self.zz,
                  self.cxx,self.cyy,self.czz,
                  0,1,0)          
        
        self.draw()
    
    
        glutSwapBuffers()
        #return


"""
Do this because if it gets put through pydoc or imported its automatically executed
"""
if __name__ == '__main__': Thing()
