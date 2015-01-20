#!/bin/python

from OpenGL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
from time import time
from math import sin, cos, pi, floor, ceil
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
    min=-5
    max=5
    value=0
    cycle=False 
    reverseloop=False
    dir=1    
    func=None
    init_tick=0
    working=True
    overide=False
    speed=1.0
    
    #defined function must return the value for storage
    def __init__(self,func=func,min=-5,max=5,cycle=False,reverseloop=False,init_tick=0):
        self.func=func
        self.min=min           
        self.max=max
        self.cycle=cycle 
        self.reverseloop=reverseloop
        self.init_tick=init_tick
        self.kick()
    
    def kick(self):    
        self.dir=1      
        self.tick=self.init_tick
        self.working=True

    def do(self):
        
        if not self.working: return
        self.tick+=self.dir*self.speed
        
        self.value=self.func((self.tick,self.value,self.min,self.max))  
                
        if self.cycle==True and self.reverseloop==False:
            if self.tick>=self.max: self.tick=self.min
            
        elif self.cycle==True and self.reverseloop==True:
            if self.tick>=self.max or self.tick<=self.min:
                self.dir*=-1
                     
        elif self.cycle==False:
            if self.tick>=self.max:
                self.working=False
                self.overide=False
                     
        if not self.value==None: return self.value
        else: return 0.0
        

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
            
    def speed_scale(self,scale):
        for a in self.actions.keys():
            self.actions[a].speed*=scale
            
    def do(self):
        for a in self.actions.keys():
            #print "do action "+str(a)
            self.actions[a].do()
            
    def value(self,action_name):
        if self.actions.has_key(action_name):
            #print "action "+str(action_name)+" "+str(self.actions[action_name].value)
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
    A_wandswish=None
    current_state="standing"
    bound=0.8 #this is his bounding sphere 
    step=0.05
    facing=1 #or -1
  
    def wobble(self,tvmm):
        t,v,mi,ma=tvmm
        v=t
        #print (t,v,mi,ma)
        return v
    
    def footR(self,tvsl):
        t,v,s,l=tvsl
        if t<7: v+=2
        elif t<10: v-=5
        else: v=0
        #print (t,v,s,l)
        return v
        
    def footL(self,tvsl):
        t,v,s,l=tvsl
        t=(t+10)%l
        if t<7: v+=2
        elif t<10: v-=5
        else: v=0
        #print (t,v,s,l)
        return v
        
    def swish(self,tvmm):
        t,v,min,max=tvmm
        v=t
        print (t,v)
        return v

    def __init__(self,sx,sy):
        self.x=sx
        self.y=sy
        
        self.AG_walk=ActionGroup()
        self.AG_walk.append("wobble",Action(func=self.wobble,max=5,cycle=True,min=-5,reverseloop=True,init_tick=0))
        self.AG_walk.append("footR",Action(func=self.footR,max=20,cycle=True,min=0))
        self.AG_walk.append("footL",Action(func=self.footL,max=20,cycle=True,min=0))
         
        self.AG_walk.speed_scale(2) 
         
        self.A_wandswish=Action(func=self.swish,min=-7,max=-1,cycle=False,reverseloop=False,init_tick=-7)
        

    def draw(self):
            
        if self.current_state=="walking":
            self.AG_walk.do()
            
        #correction
        glTranslate(0,-0.2,0)
        
        
        glTranslate(self.x,self.y,0)
        glScale(0.25,0.25,0.25)
        
        
        global X
        '''
        
        #using wobble for whole object
        #glRotatef(int( self.AG_walk.value("wobble") ),0,1,0)
        glRotatef(int(X/100)*45,0,1,0)
        '''
        if self.facing==-1: glRotatef(180,0,1,0)
        
        
        
        glRotatef(-90.0,1.0,0,0)   
        
        #hat
        glPushMatrix()
        if self.current_state=="walking": glRotatef(-float(self.AG_walk.value("wobble")),1.0,0,0)   
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
        if self.current_state=="walking": glTranslate(0-float(self.AG_walk.value("wobble"))/20,0.9,0)
        elif self.current_state=="standing" or self.current_state=="wandswish": glTranslate(0,0.9,0)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,arm)
        glutSolidSphere(0.5,24,12)            
        glPopMatrix()
        
        
        #left foot
        glPushMatrix()
        
        glTranslate(-0.5,0,0)
        if self.current_state=="walking": glRotatef(-3*float(self.AG_walk.value("footL")),0,1,0)
        elif self.current_state=="standing" or self.current_state=="wandswish": glRotatef(0,0,1,0)
        glTranslate(0.5,0,0)    
    
        glScale(2,1,.5)
        
        glTranslate(0,0.5,-2)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,shoe)
        glutSolidSphere(0.5,24,12)            
        glPopMatrix()
        
        #right foot
        glPushMatrix()
        
        glTranslate(-0.5,0,0)
        if self.current_state=="walking": glRotatef(-3*float(self.AG_walk.value("footR")),0,1,0)
        elif self.current_state=="standing" or self.current_state=="wandswish": glRotatef(0,0,1,0)
        glTranslate(0.5,0,0)    
    
          
        glScale(2,1,.5)      
        glTranslate(0,-0.5,-2)
        
        glMaterialfv(GL_FRONT,GL_DIFFUSE,shoe)
        glutSolidSphere(0.5,24,12)            
        glPopMatrix()
        
        
        
        #right arm
        glPushMatrix()
        #glTranslate(0,-0.9,0)
        if self.current_state=="wandswish":
            res=self.A_wandswish.do()
            if res==None: poo=0.0
            else: poo=float(res/0.05)
            print poo
            glTranslate(0,-0.9,0)
            glRotatef(poo,1,1,0)
            
        elif self.current_state=="walking": glTranslate(float(self.AG_walk.value("wobble"))/20,-0.9,0)
        elif self.current_state=="standing": glTranslate(0,-0.9,0)
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
        #if (X % 40)==0: self.AG_walk.kick() #ok that works
        
class Level:

    grid=None
    baddies=[]
    solomon=None
    
    AG_twinklers=None
    
    def singo(self,tvsl):
        t,v,s,l=tvsl
        v=0.5*(1+sin(2*pi*t/(l)))
        #print (t,v)
        return v
        
    def singo2(self,tvsl):
        t,v,s,l=tvsl
        v=0.5*(1+sin(4*pi*t/(l)))
        #print (t,v)
        return v
        
    
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
            
        
        self.AG_twinklers=ActionGroup()
        self.AG_twinklers.append("twinkle1",Action(func=self.singo,max=200,cycle=True,min=0,reverseloop=False,init_tick=0))
        self.AG_twinklers.append("twinkle2",Action(func=self.singo2,max=100,cycle=True,min=0,reverseloop=False,init_tick=10))
        
        
    def detect(self,xx,yy):
        
        detection=[]
        
        #print (int(floor(yy)),int(ceil(yy)))
        for rr in range(int(floor(yy)),int(ceil(yy))+1):
            #print rr
            for cc in range(int(floor(xx)),int(ceil(xx))+1):
                #print "test "+str((cc,rr))
                if (cc-xx)**2+(rr-yy)**2<(self.solomon.bound)**2:
                    c=self.grid[rr][cc]
                    #print str(c)+" at "+str((cc,rr))+" "+str((cc-xx)**2+(rr-yy)**2)+" "+str((self.solomon.bound)**2)
                    if not c in ["@","."]:
                        #print "*************************"
                        detection.append(c)
        
        '''
        rr=0
        for r in self.grid:
            cc=0
            for c in r:
                #(cc,rr)
                
                if (cc-xx)**2+(rr-yy)**2<(self.solomon.bound)**2:
                    if not c in ["@","."]:
                        #print str(c)+" at "+str((cc,rr))+" "+str((cc-xx)**2+(rr-yy)**2)+" "+str((self.solomon.bound)**2)
                        #print "*************************"
                        detection.append(c)
                
                cc+=1
                
            rr+=1
        '''    
        
        if len(detection)==0: return "OK"
        else: return detection
        
        
    def evaluate(self,joystick,keys): 
    
        self.AG_twinklers.do()
    
        if self.solomon.A_wandswish.overide==False:
        
            if joystick.isFire(keys)==True and not self.solomon.current_state=="wandswish":
            
                self.solomon.A_wandswish.kick()
                self.solomon.A_wandswish.overide=True
                self.solomon.current_state="wandswish"
        
            elif joystick.isRight(keys)==True:
            
                self.solomon.facing=1
                result=self.detect(self.solomon.x+self.solomon.step,self.solomon.y)            
                if result=="OK": self.solomon.x+=self.solomon.step
                self.solomon.current_state="walking"
                
            elif joystick.isLeft(keys)==True:
            
                self.solomon.facing=-1
                result=self.detect(self.solomon.x-self.solomon.step,self.solomon.y)                
                if result=="OK": self.solomon.x-=self.solomon.step        
                self.solomon.current_state="walking"
            
            else: self.solomon.current_state="standing"
        
    

    def draw(self):
        
        glPushMatrix()
        glTranslate(7,5.5,-0.55)
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
                
                    if c=="b": color = [0.3,0.3,1.0,1.0]
                    elif c=="s": color = [1.0,1.0,0.0,1.0]
                    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
                    glutSolidCube(1)
                    
                if c in ["d","6"]: 
                
                    glEnable(GL_BLEND)
                    glBlendFunc(GL_SRC_ALPHA, GL_SRC_ALPHA);
                    if c=="d": color = [0.8,0.5,0.0, 0.1+0.2*float(self.AG_twinklers.value("twinkle1")) ]
                    elif c=="6": color = [10,0.5,0.0, 0.1+0.2*float(self.AG_twinklers.value("twinkle1")) ]  
                    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
                    glutSolidCube( float(self.AG_twinklers.value("twinkle2"))*0.3+0.7)      
                    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
                    glDisable(GL_BLEND)
                    
                if c in ["B"]: ##i.e changed to half a block because recieved bash
                
                    #originally had this going transparent - but since the advent of DangerCode changed this to a bunch of split cubes
                    '''
                    glEnable(GL_BLEND)
                    glBlendFunc(GL_SRC_ALPHA, GL_SRC_ALPHA);
                    color =   [0.3,0.3,1.0, 0.3]
                    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
                    glutSolidCube(1)      
                    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
                    glDisable(GL_BLEND)
                    '''
                    
                    color = [0.3,0.3,1.0,1.0]
                    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
                    
                    glPushMatrix()
                    glTranslate(0.25,0.25,0.25)
                    glScale(0.4,0.44,0.44)
                    glutSolidCube(1)
                    glPopMatrix()

                    glPushMatrix()
                    glTranslate(-0.25,0.25,0.25)
                    glScale(0.44,0.44,0.34)
                    glutSolidCube(1)
                    glPopMatrix()

                    glPushMatrix()
                    glTranslate(0.25,-0.25,0.25)
                    glScale(0.44,0.44,0.34)
                    glutSolidCube(1)
                    glPopMatrix()

                    glPushMatrix()
                    glTranslate(-0.25,-0.25,0.25)
                    glScale(0.44,0.44,0.44)
                    glutSolidCube(1)
                    glPopMatrix()

                    glPushMatrix()
                    glTranslate(0.25,0.25,-0.25)
                    glScale(0.34,0.34,0.44)
                    glutSolidCube(1)
                    glPopMatrix()

                    glPushMatrix()
                    glTranslate(-0.25,0.25,-0.25)
                    glScale(0.44,0.34,0.44)
                    glutSolidCube(1)
                    glPopMatrix()

                    glPushMatrix()
                    glTranslate(0.25,-0.25,-0.25)
                    glScale(0.24,0.44,0.44)
                    glutSolidCube(1)
                    glPopMatrix()

                    glPushMatrix()
                    glTranslate(-0.25,-0.25,-0.25)
                    glScale(0.24,0.5,0.44)
                    glutSolidCube(1)
                    glPopMatrix()


                    
                glPopMatrix()
                cc+=1
                
            rr+=1
         
        self.solomon.draw()       


class Joystick:
    
    up,down,left,right,fire="","","","",""

    def __init__(self,up="q",down="a",left="o",right="p",fire="m"):
        self.up=up
        self.down=down
        self.left=left
        self.right=right
        self.fire=fire
        
    def isUp(self,keys):
        if keys.has_key(self.up): return keys[self.up]
        else: return False
         
    def isDown(self,keys):
        if keys.has_key(self.down): return keys[self.down]
        else: return False
         
    def isLeft(self,keys):
        if keys.has_key(self.left): return keys[self.left]
        else: return False
         
    def isRight(self,keys):
        if keys.has_key(self.right): return keys[self.right]
        else: return False
         
    def isFire(self,keys):
        if keys.has_key(self.fire): return keys[self.fire]
        else: return False
         
 
        
        


class SolomonsKey:

    level=None
    keys={}
    xx,yy,zz=2.5,3.0,4.5
    lastFrameTime=0
    topFPS=0
    joystick=Joystick()

    def animate(self,FPS=25):
    
        currentTime=time()
    
        try:
            if self.keys["x"]: self.xx+=0.1
            if self.keys["z"]: self.xx-=0.1
            if self.keys["d"]: self.yy+=0.1
            if self.keys["c"]: self.yy-=0.1
            if self.keys["f"]: self.zz+=0.1
            if self.keys["v"]: self.zz-=0.1
        except:
            pass 

        if not self.level==None: self.level.evaluate(self.joystick,self.keys)
        glutPostRedisplay()
        
        glutTimerFunc(int(1000/FPS), self.animate, FPS)

        drawTime=currentTime-self.lastFrameTime
        self.topFPS=int(1000/drawTime)
        if int(100*time())%100==0: print "draw time "+str(drawTime)+" top FPS "+str(1000/drawTime)
        
        self.lastFrameTime=time()


    def __init__(self):

        print bool(glutInit)
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
        glutInitWindowSize(640,480)
        glutCreateWindow(name)
        
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    
        glClearColor(0.,0.,0.,1.)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        lightZeroPosition = [10.,4.,10.,1.]
        lightZeroColor = [0.9,1.0,0.9,1.0] #green tinged
        glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.2)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
        glEnable(GL_LIGHT0)
        
        lightZeroPosition2 = [-10.,-4.,10.,1.]
        lightZeroColor2 = [1.0,0.9,0.9,1.0] #green tinged
        glLightfv(GL_LIGHT1, GL_POSITION, lightZeroPosition2)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, lightZeroColor2)
        glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 0.2)
        glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.05)
        glEnable(GL_LIGHT1)
        
        glutIgnoreKeyRepeat(1)
        
        glutSpecialFunc(self.keydownevent)
        glutSpecialUpFunc(self.keyupevent)

        glutKeyboardFunc(self.keydownevent)
        glutKeyboardUpFunc(self.keyupevent)
        glutDisplayFunc(self.display)
        #glutIdleFunc(self.display)
        
        self.animate()
        
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
            "...b@Bbbbbkb...",
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
            
        '''
        
        
        self.initkey("zxdcfvqaopm")
        
        glutMainLoop()

        return


    def initkey(self,cl):   
        for c in cl:
            self.keydownevent(c.lower(),0,0)        
            self.keyupevent(c.lower(),0,0)

    def display(self):

        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #print (self.xx,self.yy,self.zz)
        gluLookAt(self.xx,self.yy,self.zz,
                  self.xx,self.yy,self.zz-5,
                  0,1,0)
                  
        glRotatef(10,0,1,0)
        
        self.level.draw()        
        
        #print "."
        glutSwapBuffers()
        #return

    def keydownevent(self,c,x,y):
        #print (c,x,y)
        self.keys[c.lower()]=True
        glutPostRedisplay()
        

    def keyupevent(self,c,x,y):
        #print (c,x,y)
        if self.keys.has_key(c.lower()): self.keys[c.lower()]=False
        glutPostRedisplay()


if __name__ == '__main__': SolomonsKey()
