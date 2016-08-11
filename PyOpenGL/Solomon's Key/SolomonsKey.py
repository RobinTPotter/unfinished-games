#!/bin/python

from OpenGL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
from time import time
from math import sin, cos, pi, floor, ceil, sqrt
import random
from Models import lists, MakeLists, colours
from Action import Action, ActionGroup
from Joystick import Joystick

X=46.0

name = "solomon\'s key"


def key_detected_something_test(stuff):
    #print str(stuff)
    pass
    

class Sprite:

    collision_action=None
    
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.draw_func=self.temp_drawfunc        
    
        self.AG_move=ActionGroup()
        
        self.AG_move.append("x_action",Action(func=self.x_action,max=100,cycle=True,min=0))
        self.AG_move.append("y_action",Action(func=self.y_action,max=100,cycle=True,min=0)) 
        self.AG_move.append("z_action",Action(func=self.z_action,max=100,cycle=True,min=0)) 

        self.AG_move.append("xrot_action",Action(func=self.xrot_action,max=360,cycle=True,min=0))
        self.AG_move.append("yrot_action",Action(func=self.yrot_action,max=360,cycle=True,min=0)) 
        self.AG_move.append("zrot_action",Action(func=self.zrot_action,max=360,cycle=True,min=0))        

    def setDrawFuncToList(self,listid): 
        self.listnumber=listid
        self.draw_func=self.drawList

    def drawList(self):
        glCallList(self.listnumber)  
        
    def runDetection(self,level):
        level.detect(self.x,self.y,collision_bound=2.0,callback=self.collision_action,ignoreDots=True,ignoreTheseSprites=[self])   

    def draw(self):    
    
        #glPushMatrix()
        #print str((self.x,self.y))
        glTranslate(self.x,self.y,0)
        glTranslate(float(self.AG_move.value("x_action")),float(self.AG_move.value("y_action")),float(self.AG_move.value("z_action")))
        glRotate(float(self.AG_move.value("xrot_action")),1,0,0)
        glRotate(float(self.AG_move.value("yrot_action")),0,1,0)
        glRotate(float(self.AG_move.value("zrot_action")),0,0,1)   
        #glRotate(15,1,0,0)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["white"])
        #glutWireCube(1)
        self.draw_func()
        #glPopMatrix()
        
    def temp_drawfunc(self):    
        glutSolidCube(0.8)
        
        
    def do(self):
        self.AG_move.do()
        
    def x_action(self,tvmm):
        return 0
        
    def y_action(self,tvmm):
        return 0
        
    def z_action(self,tvmm):
        return 0
               
    def xrot_action(self,tvmm):
        return 0
        
    def yrot_action(self,tvmm):
        return 0
        
    def zrot_action(self,tvmm):
        t,v,min,max=tvmm
        v=t*2
        return v
               
        
def val(a,b):
    return int(100*(a+b))/100.0


class Solomon:

    x,y=None,None
    startx,starty=None,None
    #st_a=None
    AG_walk=None
    AG_jump=None
    A_wandswish=None
    current_state={}
    
    bound=0.3 #this is his bounding sphere 
    step=0.100
    facing=1 #or -1
    level=None
    
    def x_change(self,amt):
        print(("changing x",amt))
        self.x=val(self.x,amt)
        
    def y_change(self,amt):
        self.y=val(self.y,amt)    
  
    def wobble(self,tvmm):
        t,v,mi,ma=tvmm
        v=t
        #print (t,v,mi,ma)
        return v
    
    def footR(self,tvsl):
        t,v,s,l=tvsl
        if t<7: v+=1
        elif t<10: v-=2
        else: v=0
        #print (t,v,s,l)
        return v
        
    def footL(self,tvsl):
        t,v,s,l=tvsl
        if t<7: v+=1
        elif t<10: v-=2
        else: v=0
        #print (t,v,s,l)
        return v
        
    def swish(self,tvmm):
        t,v,min,max=tvmm
        v=t
        #print (t,v)
        return v
        
    def jump_displacement(self,tvmm):
        print("jump disp called")
        t,v,min,max=tvmm
        if t<4: v+=2
        else: v+=1
        return v
       
      
    def end_jump(self):
        print("jump complete")
        self.current_state["jumping"]=False

    def __init__(self,sx,sy, level):
    
        self.level=level
    
        self.current_state["standing"]=True
        self.current_state["crouching"]=False
        self.current_state["walking"]=False
        self.current_state["jumping"]=False
        self.current_state["wandswish"]=False
        self.current_state["falling"]=False
    
        self.x=sx
        self.y=sy
        
        self.startx=sx
        self.starty=sy
        
        self.AG_walk=ActionGroup()
        self.AG_walk.append("wobble",Action(func=self.wobble,max=5,cycle=True,min=-5,reverseloop=True,init_tick=0))
        self.AG_walk.append("footR",Action(func=self.footR,max=13,cycle=True,min=0))
        self.AG_walk.append("footL",Action(func=self.footL,max=13,cycle=True,min=0,init_tick=6))
        
        self.AG_jump=ActionGroup()        
        self.AG_jump.append("jump_displacement",Action(func=self.jump_displacement,max=10,min=0))        
        self.AG_jump.action("jump_displacement").callback=self.end_jump
         
        
         
        self.AG_walk.speed_scale(2) 
         
        self.A_wandswish=Action(func=self.swish,min=-7,max=-1,cycle=False,reverseloop=False,init_tick=-7)
        

    def state_test_on(self):
        return [k for k in self.current_state if self.current_state[k]==True]

    def state_test(self,list):
        return len([l for l in list if self.current_state[l]==True])


    def draw0(self):
        glTranslate(self.x,self.y,0) 
        glutSolidCube(0.1)
        

    def draw(self,stickers=None):
            
        #correction
        glTranslate(0,-0.15,0)        

        #main displacement
        glTranslate(self.x,self.y,0) 
        
        
        

        #for experiments
        global X
        #print (X,self.AG_walk.value("footL"),self.AG_walk.value("footR"))
        
        #scale down character
        glScale(0.3,0.3,0.3) 
               
        
        if stickers!=None:
            for st in stickers:
                glPushMatrix()   
                ##glLoadIdentity()
                print((st))
                glMaterialfv(GL_FRONT,GL_DIFFUSE,colours[st[3]]) 
                glTranslate(st[0]*10,10*st[1],st[2])
                glutSolidCube(0.5)      
                glPopMatrix()
                
                
        #rotate to direction facing
        if self.facing==-1: glRotatef(180,0,1,0)
        
        #correction for drawing character        
        glRotatef(-90.0,1.0,0,0)   
        
        
        
        
            
        
        
        
        drawSolProperly=True
    
    
    
        #if not drawSolProperly:        
        #    glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["white"])
        #    glutSolidCube(0.2)
            
            
        
        #############################entering crouch section###############################
        glPushMatrix()
        if "crouching" in self.state_test_on(): glTranslate(0,0,-0.3)
        
        #hat
        glPushMatrix()
        if "walking" in self.state_test_on(): glRotatef(-float(self.AG_walk.value("wobble")),1.0,0,0)   
        glTranslate(0,0,0.5)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["hat"])
        if drawSolProperly: glutSolidCone(1,2,12,6)
        glPopMatrix()
        
        #head/body
        glPushMatrix()
        glTranslate(0,0,0)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["body"])
        if drawSolProperly: glutSolidSphere(1,12,12)            
        glPopMatrix()
        
        #left arm
        glPushMatrix()
        if self.state_test(["walking"])>0: glTranslate(0-float(self.AG_walk.value("footR"))/10,0.9,0)
        elif self.state_test(["standing","crouching","wandswish"])>0: glTranslate(0,0.9,0)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["arm"])
        if drawSolProperly: glutSolidSphere(0.5,24,12)            
        glPopMatrix()
        
        
        #right arm
        glPushMatrix()
        #glTranslate(0,-0.9,0)
        if self.state_test(["wandswish"])>0:
            res=self.A_wandswish.do()
            if res==None: poo=0.0
            else: poo=float(res/0.05)
            #print poo
            glTranslate(0,-0.9,0)
            glRotatef(poo,1,1,0)
            
        elif self.state_test(["walking"])>0: glTranslate(float(self.AG_walk.value("footL"))/10,-0.9,0)
        elif self.state_test(["standing","crouching"])>0: glTranslate(0,-0.9,0)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["arm"])
        if drawSolProperly: glutSolidSphere(0.5,24,12)            
        #move pop to end to keep arm local system
        
        #wand
        q=gluNewQuadric()
        
        glPushMatrix()
        glTranslate(1.1,0,0)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["wandtip"])
        glRotatef(90,0,1,0) 
        if drawSolProperly: gluCylinder(q,0.1,0.1,0.2,12,1)            
        glPopMatrix()
        
        glPushMatrix()
        glTranslate(0.5,0,0)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["wand"])
        glRotatef(90,0,1,0) 
        if drawSolProperly: gluCylinder(q,0.1,0.1,0.6,12,1)            
        glPopMatrix()
        
        #from arm
        glPopMatrix()
        
        #eyes
        glPushMatrix()
        glTranslate(1,.2,.1)
        glRotatef(90,0,1,0)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["wandtip"])    
        if drawSolProperly: gluDisk(q,0.05,0.2,12,12)           
        glPopMatrix()
        
        glPushMatrix()    
        glTranslate(1,-.2,.1)
        glRotatef(90,0,1,0)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["wandtip"])    
        if drawSolProperly: gluDisk(q,0.05,0.2,12,12)           
        glPopMatrix()
        
        #nose    
        glPushMatrix()
        glTranslate(1,0,-.1)
        glScale(1,1,0.5)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["arm"])
        if drawSolProperly: glutSolidSphere(0.3,24,12)            
        glPopMatrix()
        
        ##########################left crouch section##################################
        glPopMatrix() #end of crouch
                
        #drawing rest of body (feet)
        #left foot
        glPushMatrix()        
        glTranslate(-0.5,0,0)
        #apply rotation if walking
        if self.state_test(["walking"])>0: glRotatef(-15*float(self.AG_walk.value("footL")),0,1,0)
        elif self.state_test(["standing","crouching","wandswish"])>0: glRotatef(0,0,1,0)
        glTranslate(0.5,0,0)        
        glScale(1.5,1,.5)        
        glTranslate(0,0.5,-2)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["shoe"])
        if drawSolProperly: glutSolidSphere(0.5,24,12)            
        glPopMatrix()
        
        #right foot
        glPushMatrix()        
        glTranslate(-0.5,0,0)
        #apply rotation if walking
        if self.state_test(["walking"])>0: glRotatef(-15*float(self.AG_walk.value("footR")),0,1,0)
        elif self.state_test(["standing","crouching","wandswish"])>0: glRotatef(0,0,1,0)
        glTranslate(0.5,0,0)             
        glScale(1.5,1,.5)      
        glTranslate(0,-0.5,-2)        
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["shoe"])
        if drawSolProperly: glutSolidSphere(0.5,24,12)            
        glPopMatrix()
        
        
        
        
        X+=1
        #if (X % 40)==0: self.AG_walk.kick() #ok that works
        
class Level:

    grid=None
    baddies=[]
    solomon=None
    sprites=[]
    
    AG_twinklers=None
    
    def sin_gen_1(self,tvsl):
        t,v,s,l=tvsl
        v=0.5*(1+sin(2*pi*t/(l)))
        #print (t,v)
        return v
        
    def sin_gen_2(self,tvsl):
        t,v,s,l=tvsl
        v=0.5*(1+sin(4*pi*t/(l)))
        #print (t,v)
        return v        
    
    def __init__(self,griddata):
    
        griddata.reverse()
        
        #self.grid=griddata
        self.grid=[]
        for line in griddata:
            self.grid.append(list(line))
            
        rr=0
        for r in self.grid:
            cc=0
            for c in r:
                if c=="@":
                    self.solomon=Solomon(cc,rr,self)
                    self.grid[rr][cc]="."
                    self.solomon.A_wandswish.callback=self.block_swap
                    
                elif c=="k":
                    ns=Sprite(cc,rr)
                    ns.setDrawFuncToList(lists["green_key"])
                    ns.collision_action=key_detected_something_test
                    self.sprites.append(ns)
                    self.grid[rr][cc]="."
                    
                
                elif not c in ["b","B","s"]:
                    self.grid[rr][cc]="."

                cc+=1
                
            rr+=1                    
        
        self.AG_twinklers=ActionGroup()
        self.AG_twinklers.append("twinkle1",Action(func=self.sin_gen_1,max=200,cycle=True,min=0,reverseloop=False,init_tick=0))
        self.AG_twinklers.append("twinkle2",Action(func=self.sin_gen_2,max=100,cycle=True,min=0,reverseloop=False,init_tick=10))
        
        
    def block_swap(self):
    
        print("hi"+str(self.solomon))
        takeoff_for_crouching=0
        if self.solomon.state_test(["crouching"])>0 : takeoff_for_crouching=-0.8
        res=self.detect(val(self.solomon.x,self.solomon.facing*1.0),val(self.solomon.y,takeoff_for_crouching),collision_bound=0.5)
                
        if res=="OK": return
        
        ch,xx,yy,dist=res[0]
        if ch=="b":
            #print("break block")
            #self.grid[yy][xx]="B"   
            print("destroy block")
            self.grid[yy][xx]="."            
        elif ch=="B":
            print("destroy block")
            self.grid[yy][xx]="."      
        elif ch==".":
            print("create")
            self.grid[yy][xx]="b"
            
        
    def detect(self,xx,yy,collision_bound=None,callback=None,ignoreDots=False,ignoreTheseSprites=[]):
        """ return "OK" message in test of a tuple of (character detected,x of char,y of char,distance float """
        
        if collision_bound==None: collision_bound=self.solomon.bound
        
        detection=[]
        
        for rr in range(int(floor(yy-collision_bound+0.5)),int(ceil(yy+collision_bound+0.5))): #didhave +1
            list1=""
            
            for cc in range(int(floor(xx-collision_bound+0.5)),int(ceil(xx+collision_bound+0.5))):
                c=self.grid[rr][cc]
                if not (c=="." and ignoreDots==True):
                    test=(cc-xx)**2+(rr-yy)**2
                    list1+=c
                    if test<(collision_bound)**2:
                        detection.append((c,cc,rr,sqrt(test)))
                        
            #print list1  
        
        for s in self.sprites:
            if not s in ignoreTheseSprites:
                test=(s.x-xx)**2+(s.y-yy)**2
                if test<(collision_bound)**2:
                    detection.append((s,s.x,s.y,sqrt(test)))
                    
        
        detection=sorted(detection,key=lambda x: x[3])  

        if not callback==None: callback(detection)
              
        return detection
        
    
    def evaluate(self,joystick,keys): 
    
    
        
        self.solomon.stickers=[]
        
        self.solomon.stickers.append([0,0,0,"white"])
        
        """ TODO redo current_state was rubbish anyway """
        
        self.AG_twinklers.do() 
        
        
        
        jumpnow=False
        walkcheck=False        
        
        if self.solomon.A_wandswish.overide==False:
        
            self.solomon.current_state["wandswish"]=False  

            if joystick.isDown(keys)==True:                    
                self.solomon.current_state["crouching"]=True                        
                self.solomon.current_state["standing"]=False
            else:     
                self.solomon.current_state["crouching"]=False               
                    
                if joystick.isRight(keys)==True:
                    self.solomon.facing=1    
                    self.solomon.current_state["walking"]=True
                    self.solomon.current_state["standing"]=False                    
                    walkcheck=True                        
                elif joystick.isLeft(keys)==True:                
                    self.solomon.facing=-1    
                    self.solomon.current_state["walking"]=True
                    self.solomon.current_state["standing"]=False    
                    walkcheck=True
                else:
                    self.solomon.current_state["walking"]=False                
                    self.solomon.current_state["standing"]=True                    
            
            if walkcheck==True:
                if joystick.isUp(keys)==True and self.solomon.current_state["jumping"]==False:
                    self.solomon.current_state["jumping"]=True
                    jumpnow=True
                else:
                    self.solomon.current_state["jumping"]=False



            xcheck_p=val(self.solomon.x+0.5,self.solomon.step*2*self.solomon.facing)
            xcheck_m=val(self.solomon.x+0.5,-self.solomon.step*2*self.solomon.facing)
            
            #self.solomon.stickers.append([xcheck_p,self.solomon.y-self.solomon.step,0,"white"])
            #self.solomon.stickers.append([xcheck_m,self.solomon.y-self.solomon.step,0,"white"])
        

            #self.solomon.stickers.append([xcheck_p,self.solomon.y-self.solomon.step,0,"white"])
            #self.solomon.stickers.append([xcheck_m,self.solomon.y-self.solomon.step,0,"white"])
        
        
            width=1.5
        
            canwalk=False
            
            
            
            if walkcheck:           
            
            
                col="green"
                if self.solomon.facing==-1:
                    col="yellow"
                    
                self.solomon.stickers.append([self.solomon.facing*self.solomon.step*width,0,0,col])
                
                result=self.detect(val(self.solomon.x,self.solomon.facing*self.solomon.step*width),self.solomon.y)      
                
                
                
                           
                if (len(result)==0 or result[0][0]==".") and self.solomon.current_state["walking"]==True:
                    #self.solomon.x+=self.solomon.step*self.solomon.facing                
                    self.solomon.current_state["standing"]=False  
                    self.solomon.current_state["walking"]=True
                    canwalk=True
                #elif result[0][0] in ["]

            
            result1=self.grid[int(self.solomon.y-self.solomon.step)][int(xcheck_p)]
            result2=self.grid[int(self.solomon.y-self.solomon.step)][int(xcheck_m)]
            print("fall check" + str((result1,result2,self.solomon.x,self.solomon.y)))
            if result1=="." and result2==".":
                self.solomon.y_change(-self.solomon.step)
                print(("solomon y affected by", -self.solomon.step))
                self.solomon.current_state["falling"]=True
                #canwalk=False
            else:
                self.solomon.current_state["falling"]=False
            

            if canwalk==True:
                print(("self.solomon.x before",self.solomon.x))
                self.solomon.x_change(self.solomon.step*self.solomon.facing)
                print(("self.solomon.x after",self.solomon.x))

            if joystick.isFire(keys)==True and self.solomon.current_state["wandswish"]==False:            
                self.solomon.A_wandswish.kick()
                self.solomon.A_wandswish.overide=True
                self.solomon.current_state["wandswish"]=True 

                    
        if self.solomon.current_state["jumping"]==True:  
            isWalk=0
            if self.solomon.current_state["walking"]==True: isWalk=1
            result=self.detect(self.solomon.x+(self.solomon.facing*self.solomon.step*5.0)*(isWalk),self.solomon.y)     
            
            self.solomon.current_state["falling"]=False
            print(("jumping",result))
            self.solomon.AG_jump.do()
            print("he's jumping")
            print(str(self.solomon.AG_jump.action("jump_displacement").tick  ))
            print(str(self.solomon.AG_jump.action("jump_displacement").value  ))
            self.solomon.y+=0.2
            print(("solomon y affected by", +0.2))
            #print "co-ordinates "+str((self.solomon.x,self.solomon.y))

        if joystick.isUp(keys)==True and self.solomon.current_state["jumping"]==False:                    
            self.solomon.current_state["jumping"]=True
            self.solomon.AG_jump.kick()


        if self.solomon.current_state["walking"]==True:
            self.solomon.AG_walk.do()
            


    def draw(self):
    
        #global X
        #glRotate(X,1,0,0)
        
        glPushMatrix()
        glTranslate(8,6.5,-0.55)
        glScale(15,12,0.1)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["red"])
        glutSolidCube(1)        
        glPopMatrix()
        
        rr=0
        for r in self.grid:
            cc=0
            for c in r:
                #if True:
                if rr>0 and rr<13 and cc>0 and cc<16:
                    
                    glPushMatrix()
                    glTranslate(cc,rr,0)
                    
                    if c in ["b","s"]: 
                    
                        if c=="b": color = [0.3,0.3,1.0,1.0]
                        elif c=="s": color = [1.0,1.0,0.0,1.0]
                        glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
                        glutWireCube(1)
                        #glutSolidCube(1)
                        
                    elif c in ["d","6"]: 
                    
                        glEnable(GL_BLEND)
                        glBlendFunc(GL_SRC_ALPHA, GL_SRC_ALPHA);
                        if c=="d": color = [0.8,0.5,0.0, 0.1+0.2*float(self.AG_twinklers.value("twinkle1")) ]
                        elif c=="6": color = [10,0.5,0.0, 0.1+0.2*float(self.AG_twinklers.value("twinkle1")) ]  
                        glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
                        glutSolidCube( float(self.AG_twinklers.value("twinkle2"))*0.3+0.7)      
                        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
                        glDisable(GL_BLEND)
                        
                    elif c in ["B"]: ##i.e changed to half a block because recieved bash
                        
                        color = [0.3,0.3,1.0,1.0]
                        glMaterialfv(GL_FRONT,GL_DIFFUSE,color)                                        
                        #global lists
                        glCallList(lists["broken brick"])        

                   

          
                        
                    glPopMatrix()

                cc+=1
                
            rr+=1
         
        glPushMatrix()
        self.solomon.draw(self.solomon.stickers)  
        glPopMatrix()
        
        
        

        
        for s in self.sprites:
            glPushMatrix()
            s.runDetection(self)
            s.draw()
            glPopMatrix()
            s.do()
    




         
class SolomonsKey:

    level=None
    keys={}
    cxx,cyy,czz=8,6.5,15 #2.5,5.0,15
    tcxx,tcyy,tczz=0,0,0    
    fxx,fyy,fzz=8,6.5,0 #0,0,0
    tfxx,tfyy,tfzz=0,0,0
    
    lastFrameTime=0
    topFPS=0
    joystick=Joystick()

    def animate(self,FPS=25):
    
        currentTime=time()
    
        try:
            if self.keys["x"]: self.fxx+=1
            if self.keys["z"]: self.fxx-=1
            if self.keys["d"]: self.fyy+=1
            if self.keys["c"]: self.fyy-=1
            if self.keys["f"]: self.fzz+=1
            if self.keys["v"]: self.fzz-=1
        except:
            pass 

        if not self.level==None: self.level.evaluate(self.joystick,self.keys)
        glutPostRedisplay()
        
        glutTimerFunc(int(1000/FPS), self.animate, FPS)

        drawTime=currentTime-self.lastFrameTime
        self.topFPS=int(1000/drawTime)
        if int(10*time())%10==0:
        
            print("draw time "+str(drawTime)+" top FPS "+str(1000/drawTime)     )
            '''
            gr=0

            print(("solomon",self.level.solomon.x,self.level.solomon.y))
            for gg in range(len(self.level.grid)-1,-1,-1):
                temp=list(self.level.grid[gg])
                
                if int(self.level.solomon.y)==gg: temp[int(self.level.solomon.x)]="#"
                print((temp),"\n")
            #self.tcxx,self.tcyy,self.tczz=random.randint(5,14),random.randint(5,14),random.randint(5,14)
            print("","\n")
            '''
        
        self.tfxx,self.tfyy,self.tfzz=self.level.solomon.x,self.level.solomon.y,5
        self.tcxx,self.tcyy,self.tczz=self.level.solomon.x,self.level.solomon.y,18
            
        self.cxx+=(self.tcxx-self.cxx)/25
        self.cyy+=(self.tcyy-self.cyy)/25
        self.czz+=(self.tczz-self.czz)/25
        
        self.fxx+=(self.tfxx-self.fxx)/25
        self.fyy+=(self.tfyy-self.fyy)/25
        self.fzz+=(self.tfzz-self.fzz)/25        

        self.lastFrameTime=time()

    def __init__(self):

        print(str(bool(glutInit)))
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
        
        MakeLists()
        
        glutIgnoreKeyRepeat(1)
        
        glutSpecialFunc(self.keydownevent)
        glutSpecialUpFunc(self.keyupevent)

        glutKeyboardFunc(self.keydownevent)
        glutKeyboardUpFunc(self.keyupevent)
        glutDisplayFunc(self.display)
        #glutIdleFunc(self.display)
        
        glMatrixMode(GL_PROJECTION)
        gluPerspective(60.0,640.0/480.,1.,50.)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        
        '''
        self.level=Level([
            ".sssssssssssssss.",
            "s...............s",
            "s.......d.......s",
            "s......@........s",
            "s....bsbbbs.....s",
            "s...b.b343b.....s",
            "s..b..sbbbs..g..s",
            "s......bbb......s",
            "s...2.......2...s",
            "s.b.sbs.1.sbs...s",
            "s.bbbb...b.bbb..s",
            "s..b.bbbb.b.....s",
            "sb.......b......s",
            ".sssssssssssssss."])
        '''
        
        self.level=Level([
            ".sssssssssssssss.",
            "s...............s",
            "s.......d.......s",
            "s.5.............s",
            "s.....sbbbs.....s",
            "s.....b343b.....s",
            "s..g..sbbbs..g..s",
            "s......bbb......s",
            "s...2.......2...s",
            "s...sbs.1.sbs...s",
            "s...b@bbbbbkb...s",
            "s...sbs...sbs...s",
            "s...............s",
            ".sssssssssssssss."])
        
        '''
        self.level=Level([
            "sssssssssssssssss",
            "s...............s",
            "s.6.6...........s",
            "s.......4.....k.s",
            "s.ss.........bb.s",
            "s...ss.....bb...s",
            "s.....ss.bb.....s",
            "s...............s",
            "s.....bbbss.....s",
            "s.@.bbbbbbbss.d.s",
            "s.bb.........ss.s",
            "s...............s",
            "s...............s",
            "sssssssssssssssss"]
            
        '''
        '''
        self.level=Level([
            "sssssssssssssssss",
            "s...............s",
            "s...............s",
            "s...............s",
            "s...............s",
            "s...............s",
            "s...............s",
            "s...............s",
            "s...............s",
            "s.......@.......s",
            "s...............s",
            "s...............s",
            "s...............s",
            "sssssssssssssssss"]
            
        '''
        
        
        self.initkey("zxdcfvqaopm")
        
        self.animate()
        
        glutMainLoop()

        return


    def initkey(self,cl):   
    
        for c in cl:
            self.keydownevent(c.lower(),0,0)        
            self.keyupevent(c.lower(),0,0)

    def display(self):


        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        gluLookAt(self.cxx,self.cyy,self.czz,
                  self.fxx,self.fyy,self.fzz,
                  0,1,0)
        
        #gluLookAt(10*cos(2*pi*self.lastFrameTime/10.0),10*sin(2*pi*self.lastFrameTime/50.0),10*sin(2*pi*self.lastFrameTime/10.0),
        #          self.fxx,self.fyy,self.fzz,
        #          0,1,0)
        
        
        
        self.level.draw()
        print("DISPlAY")
        
        
     
     
     
        glLoadIdentity()
        
        
        gluLookAt(0, -0.5, 2.5,
                  0, 0, 0  ,
                  0, 1, 0  )
        
        
        wdth=0.3
        glTranslate(0.0-(len(self.level.solomon.current_state.keys())-1)*wdth/2.0,-1.3,0)  

        for k in self.level.solomon.current_state.keys():
            col="red"
            if self.level.solomon.current_state[k]: col="green"
            glMaterialfv(GL_FRONT,GL_DIFFUSE,colours[col])      
            glutSolidCube(wdth-0.02)
            glTranslate(wdth,0,0)
            
     
     
        glLoadIdentity()
        
        
        gluLookAt(0, -0.5, 2.5,
                  0, 0, 0  ,
                  0, 1, 0  )
        
        wdth=0.2
       
        list=[x for x in dir(self.joystick) if x[0:2]=="is"]
        glTranslate(0.0-(len(list)-1)*wdth/2.0,-1.0,0)  

        for k in list:
            print(k)
                        
            col="red"
            if getattr(self.joystick,k)(self.keys): col="green"
            glMaterialfv(GL_FRONT,GL_DIFFUSE,colours[col])      
            glutSolidCube(wdth-0.02)
            glTranslate(wdth,0,0)
            
     
        
        
        
        
        
        
        
        
        
        glutSwapBuffers()

    def keydownevent(self,c,x,y):
        try:
            self.keys[c.lower()]=True
        except:
            pass

        glutPostRedisplay()
        
    def keyupevent(self,c,x,y):
    
        try: 
            if self.keys.has_key(c.lower()): self.keys[c.lower()]=False
        except:
            pass

        glutPostRedisplay()
        
if __name__ == '__main__': SolomonsKey()