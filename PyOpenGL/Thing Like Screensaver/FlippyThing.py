

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import random 
import sys
from time import time

name = "thing"

colours={}
colours["red"]=[1.0,0.0,0.0,1.0]
colours["green"]=[0.0,1.0,0.0,1.0]
colours["blue"]=[0.0,0.0,1.0,1.0]
colours["yellow"]=[1.0,1.0,0.0,1.0]
colours["cyan"]=[0.0,1.0,1.0,1.0]
colours["white"]=[1.0,1.0,1.0,1.0]

class Tile:
    
    x,y=None,None #current position
    hinge=None # side hinge is on currently
    state=0 #between 0 anf 1 for state of rotration 0 at rest always
    turning=0
    colour=None
    controller=None
    
    def __init__(self,x,y,controller):
        self.x,self.y=x,y  
        col=random.randint(0,len(colours)-1)
        self.colour=colours.keys()[col]
        self.controller=controller
        
    def have_turn(self,hinge):
        self.hinge=hinge
        self.state=0.0
        self.turning=1
        
    def draw(self):
    
    
    
    
        glPushMatrix() 
        glTranslate(self.x,self.y,0)   
        
        #print "drawing "+str(self.hinge)+" "+str(self.state)
        
        
        if self.turning==1:
            glRotate(90*self.hinge,0,0,1)
            glRotate(180*self.state,0,1,0)
            glTranslate(-1,0,0)
        
            
                
            
                 
        glScale(0.95,0.95,0.1)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours[self.colour])
        glutSolidCube(1) 

        #glTranslate(1,0,0)                  
        glPopMatrix()

        
        
                
        if self.turning==1:
        
            self.state+=0.01
            
            if self.state>1.0:
                self.state=0
                self.turning=0
                print "done "+str(self.hinge)
                self.controller.next()
                
             
                if self.hinge==0:
                    self.x-=1
                elif self.hinge==1:
                    self.y-=1
                elif self.hinge==2:
                    self.x+=1
                elif self.hinge==3:
                    self.y+=1
            
                

            
            
        
        
    

class Thing:

    tiles=[]
    
    lastFrameTime=0
    
    xx,yy,zz=3,1,2

    def draw(self,FPS=1):
        
        
        currentTime=time()
        
        '''
        glPushMatrix()     
        glTranslate(0,0,0)
        glScale(1,1,1)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["white"])
        glutSolidCube(1)                   
        glPopMatrix()
        '''
        
        
        glPushMatrix()     
        for t in self.tiles: t.draw()
        glPopMatrix()
        
        
        glutPostRedisplay()
        
        
        
        #glutTimerFunc(int(1000/FPS), self.draw, FPS)

        #drawTime=currentTime-self.lastFrameTime
        #self.topFPS=int(1000/drawTime)
        #if int(100*time())%100==0: print "draw time "+str(drawTime)+" top FPS "+str(1000/drawTime)
        
        

    def isTileHere(self,xx,yy):
        for t in self.tiles:
            if t.x==xx and t.y==yy:
                return t
        
        return None
        

    def next(self):
    
        #random.shuffle(self.tiles)
        
        holes=[]
        for t in self.tiles:
            if self.isTileHere(t.x-1,t.y)==None: holes.append([t,t.x-1,t.y,0])
            if self.isTileHere(t.x+1,t.y)==None: holes.append([t,t.x+1,t.y,2])
            if self.isTileHere(t.x,t.y-1)==None: holes.append([t,t.x,t.y-1,1])
            if self.isTileHere(t.x,t.y+1)==None: holes.append([t,t.x,t.y+1,3])
            
        next_hole=random.randint(0,len(holes)-1)
        holes[next_hole][0].have_turn(holes[next_hole][3])
             
        


    def __init__(self):   
     
        for xx in range(0,10):
            for yy in range(0,10):
                if random.randint(0,20)>0: self.tiles.append(Tile(xx,yy,self))
                
            
        #print str(self.tiles)
        self.next()
        
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
        gluPerspective(90.0,640.0/480.,1.,50.)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glutMainLoop()
        
        return

    def display(self):

        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #print (self.xx,self.yy,self.zz)
        gluLookAt(self.xx,self.yy,self.zz,
                  5,5,0,
                  0,1,0)
                  
        glRotatef(10,0,1,0)
        
                  
        glPushMatrix()     
        self.draw()
        glPopMatrix()
    
    
        glutSwapBuffers()
        #return



if __name__ == '__main__': Thing()
