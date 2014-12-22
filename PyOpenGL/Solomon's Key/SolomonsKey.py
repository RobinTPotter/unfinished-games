#!/bin/python

from OpenGL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

X=46.0

name = "solomon\'s key"
red=[1.0,0.0,0.0,1.0]
green=[0.0,1.0,0.0,1.0]
blue=[0.0,0.0,1.0,1.0]
hat=[0.105,0.097,0.107,1.0]
body=[0.093,0.02,0.0006071,1.0]
arm=[0.24,0.007,0.0,1.0]
shoe=[0.096,0.0,1.0]
wand=[0,0,0,1.0]
wandtip=[1,1,1,1.0]



class Baddie:
    def __init__(self,type):
        pass


class Action:
    
    tick=0
    value=0
    last=-1
    cycle=False 
    start=0
    loop=False
    dir=1    
    func=None
    
    #defined function must return the value for storage
    def __init__(self,func=func,end=-1,cycle=False,start=0,loop=False):
        self.func=func
        self.last=end     
        self.cycle=cycle       
        self.start=start
        self.loop=loop
        self.kick()
    
    def kick(self):    
        self.tick=self.start    

    def do(self):
        if self.cycle==True:
            if self.loop==False:
                if self.tick>self.last: self.tick=self.start-1
            elif self.loop==True:
                if self.tick>self.last or self.tick<self.start: self.dir*=-1 
           
        else:
            if self.tick>=self.last: return self.start
            
        self.tick+=self.dir        
        
        self.value=self.func((self.tick,self.value,self.start,self.last))
        
        return self.value
        

#defines a set of actions to be done as one.
class ActionGroup:

    actions={}

    def __init__(self):
        self.actions={}
        
    def append(self,action_name,action):
        if self.actions.has_key(action_name):
            raise Error("action defined "+action_name)
        else:
            self.actions[action_name]=action
            
        
    def kick(self):
        for a in self.actions.keys():
            self.actions[a].kick()
            
    def do(self):
        for a in self.actions.keys():
            self.actions[a].do()
            
    def value(self,action_name):
        if self.actions.has_key(action_name):
            return self.actions[action_name].value
        else:
            raise Error("no such action registered "+action_name)
            
    def action(self,action_name):
        if self.actions.has_key(action_name):
            return self.actions[action_name]
        else:
            raise Error("no such action registered "+action_name)
            

class Solomon:

    x,y=None,None
    #st_a=None
    AG_walk=None
    
    def wobble(self,tvsl):
        t,v,s,l=tvsl
        v=t
        #print (t,v,s,l)
        return v
    
    def footL(self,tvsl):
        t,v,s,l=tvsl
        if t<7: v=t
        else: v=6+l-t
        #print (t,v,s,l)
        return v

    def __init__(self,sx,sy):
        self.x=sx
        self.y=sy
        self.AG_walk=ActionGroup()
        self.AG_walk.append("wobble",Action(self.wobble,10,False,start=-10))
        self.AG_walk.append("footL",Action(self.footL,10,False,start=0))
        
        

    def draw(self):
            
        self.AG_walk.do()


        #correction
        glTranslate(0,-0.2,0)
        
        
        glTranslate(self.x,self.y,0)
        glScale(0.25,0.25,0.25)
        
        global X
        
        #using wobble for whole object
        glRotatef(int( self.AG_walk.value("wobble") ),0,1,0)
        #glRotatef(X,0,1,0)
        
        
        
        
        
        glRotatef(-90.0,1.0,0,0)    
        
        #hat
        glPushMatrix()
        glTranslate(0,0,0.5)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,hat)
        glutSolidCone(1,2,12,6)
        glPopMatrix()
        
        #head/body
        glPushMatrix()
        glTranslate(0,0,0)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,body)
        glutSolidSphere(1,12,12)            
        glPopMatrix()
        
        #left arm
        glPushMatrix()
        glTranslate(0,0.9,0)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,arm)
        glutSolidSphere(0.5,24,12)            
        glPopMatrix()
        
        
        #left foot
        glPushMatrix()
        glScale(2,1,.5)
        
        glTranslate(0,0.5,-2)
        glRotatef(int(self.AG_walk.value("footL")),0,0,1)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,shoe)
        glutSolidSphere(0.5,24,12)            
        glPopMatrix()
        
        #right foot
        glPushMatrix()
        glScale(2,1,.5)
        
        glTranslate(0,-0.5,-2)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,shoe)
        glutSolidSphere(0.5,24,12)            
        glPopMatrix()
        
        
        
        #right arm
        glPushMatrix()
        glTranslate(0,-0.9,0)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,arm)
        glutSolidSphere(0.5,24,12)            
        #move pop to end to keep arm local system
        
        #wand
        q=gluNewQuadric()
        
        glPushMatrix()
        glTranslate(1.1,0,0)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,wandtip)
        glRotatef(90,0,1,0) 
        gluCylinder(q,0.1,0.1,0.2,12,1)            
        glPopMatrix()
        
        glPushMatrix()
        glTranslate(0.5,0,0)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,wand)
        glRotatef(90,0,1,0) 
        gluCylinder(q,0.1,0.1,0.6,12,1)            
        glPopMatrix()
        
        #from arm
        glPopMatrix()
        
        #eyes
        glPushMatrix()
        glTranslate(1,.2,.1)
        glRotatef(90,0,1,0)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,wandtip)    
        gluDisk(q,0.05,0.2,12,12)           
        glPopMatrix()
        
        glPushMatrix()    
        glTranslate(1,-.2,.1)
        glRotatef(90,0,1,0)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,wandtip)    
        gluDisk(q,0.05,0.2,12,12)           
        glPopMatrix()
        
        #nose    
        glPushMatrix()
        glTranslate(1,0,-.1)
        glScale(1,1,0.5)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,arm)
        glutSolidSphere(0.3,24,12)            
        glPopMatrix()
        
        X+=1
        #if X==100: self.st_a.kick() #ok that works
        
class Level:
    grid=None
    baddies=[]
    solomon=None
    
    def __init__(self,griddata):
        griddata.reverse()
        self.grid=griddata
        
        rr=0
        for r in self.grid:
            cc=0
            for c in r:
                if c=="@":
                    self.solomon=Solomon(cc,rr)
                
                cc+=1
                
            rr+=1
        

    def draw(self):
        
        glPushMatrix()
        glTranslate(7,5.5,-0.5)
        glScale(15,12,0.1)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,red)
        glutSolidCube(1)        
        glPopMatrix()
        
        rr=0
        for r in self.grid:
            cc=0
            for c in r:
                glPushMatrix()
                glTranslate(cc,rr,0)
                if c in ["b","s"]: 
                    if c=="b": color = [0.5,0.5,1.0,1.0]
                    elif c=="s": color = [1.0,1.0,0.0,1.0]
                    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
                    glutSolidCube(1)
                    
                glPopMatrix()
                cc+=1
                
            rr+=1
                

class SolomonsKey:

    level=None
    keys={}
    xx,yy,zz=2.5,3.0,4.5
    

    def __init__(self):

        print bool(glutInit)
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(640,480)
        glutCreateWindow(name)

        glClearColor(0.,0.,0.,1.)
        glShadeModel(GL_SMOOTH)
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
        
        
        '''
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
        '''
        
        self.level=Level([
            "...............",
            ".6.6...........",
            ".......4.....k.",
            ".ss.........bb.",
            "...ss.....bb...",
            ".....ss.bb.....",
            "...............",
            ".....bbbss.....",
            ".@.bbbbbbbss.d.",
            ".bb.........ss.",
            "...............",
            "..............."])

        glutMainLoop()

        return

    def display(self):

        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #print (self.xx,self.yy,self.zz)
        gluLookAt(self.xx,self.yy,self.zz,
                  self.xx,self.yy,self.zz-5,
                  0,1,0)
                  
        glRotatef(10,0,1,0)
        
        
        self.level.draw()        
        self.level.solomon.draw()
        
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
        print (c,x,y)
        self.keys[c]=True

    def keyupevent(self,c,x,y):
        #print (c,x,y)
        if self.keys.has_key(c): self.keys[c]=False


if __name__ == '__main__': SolomonsKey()
