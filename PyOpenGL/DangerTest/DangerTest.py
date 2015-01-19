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
#colours["yellow"]=[1.0,1.0,0.0,1.0]
#colours["cyan"]=[0.0,1.0,1.0,1.0]
#colours["white"]=[1.0,1.0,1.0,1.0]
  
class Thing:

    lastFrameTime=0
    
    xx,yy,zz=0,0,10
    cxx,cyy,czz=0,0,0
    X=0

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
        
    def draw(Self):
    
        
        glPushMatrix()     
        ##for t in self.tiles: t.draw()
        f=open("DangerCode.txt","r")
        code=f.read()
        print "DC:"+code
        exec(code)
        
        glPopMatrix()
                 

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
        
        '''
        glutSpecialFunc(self.keydownevent)
        glutSpecialUpFunc(self.keyupevent)
        glutKeyboardFunc(self.keydownevent)
        glutKeyboardUpFunc(self.keyupevent)
        '''
        
        glutDisplayFunc(self.display)
        #glutIdleFunc(self.display)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(110.0,640.0/480.,1.,50.)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        
        self.animate(FPS=20)
        
        glutMainLoop()
        
        
        return

    def display(self):

        glEnable (GL_BLEND)
        glEnable (GL_POLYGON_SMOOTH)
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #print (self.xx,self.yy,self.zz)                 
        
        gluLookAt(self.xx,self.yy,self.zz,
                  self.cxx,self.cyy,self.czz,
                  0,1,0)          
        
        glPushMatrix()     
        self.draw()
        glPopMatrix()
    
    
        glutSwapBuffers()
        #return


"""
Do this because if it gets put through pydoc or imported its automatically executed
"""
if __name__ == '__main__': Thing()
