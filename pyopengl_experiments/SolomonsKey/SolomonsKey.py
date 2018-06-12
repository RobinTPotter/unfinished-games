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
from Sprite import Sprite
import Letters


X=46.0

name = "solomon\'s key"
debug=True

def dump(thing):
    print thing.__dict__
    
class Solomon:

    x,y=None,None
    startx,starty=None,None
    #st_a=None
    AG_walk=None
    AG_jump=None
    A_wandswish=None
    current_state={}
    jumping_counter = 0
    jumping_counter_max = 7
    jump_inc_start = 0.5
    jump_inc = 0.2
    jump_inc_falloff = 0.6
    step_inc = 0.05
    jumping_dir=0
    jumping_rest=0
    jumping_rest_start=2 ##cycles to rest before jump
    wand_rest=0
    wand_rest_start=8 ##cycles to rest before jump
    

    bound=0.3 #this is his bounding sphere
    step=0.100
    facing=1 #or -1
    level=None

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
        #print ('footR',t,v,s,l)
        return v

    def footL(self,tvsl):
        t,v,s,l=tvsl
        if t<7: v+=1
        elif t<10: v-=2
        else: v=0
        #print ('footL' ,t,v,s,l)
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
        self.AG_walk.append("footR",Action(func=self.footR,max=13,cycle=True,min=-1))
        self.AG_walk.append("footL",Action(func=self.footL,max=13,cycle=True,min=-1,init_tick=7))

        self.AG_jump=ActionGroup()
        self.AG_jump.append("jump_displacement",Action(func=self.jump_displacement,max=10,min=0))
        self.AG_jump.action("jump_displacement").callback=self.end_jump



        self.AG_walk.speed_scale(2)

        self.A_wandswish=Action(func=self.swish,min=-8,max=-1,cycle=False,reverseloop=False,init_tick=-4)


    def state_test_on(self):
        return [k for k in self.current_state if self.current_state[k]==True]

    def state_test(self,list):
        return len([l for l in list if self.current_state[l]==True])


    def draw0(self):
        glTranslate(self.x,self.y,0)
        glutSolidCube(0.1)


    def draw(self,stickers=None):

        drawSolProperly=True

        if drawSolProperly:
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
                #print((st))
                glMaterialfv(GL_FRONT,GL_DIFFUSE,colours[st[3]])
                glTranslate(st[0]*10,10*st[1],st[2])
                glutSolidCube(0.5)
                glPopMatrix()


        #rotate to direction facing
        if self.facing==-1: glRotatef(180,0,1,0)

        #correction for drawing character
        glRotatef(-90.0,1.0,0,0)


        #if not drawSolProperly:
        #    glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["white"])
        #    glutSolidCube(0.2)



        #############################entering crouch section###############################
        glPushMatrix()
        if "crouching" in self.state_test_on(): glTranslate(0,0,-0.4)


        #if "walking" in self.state_test_on(): glRotatef(0.0,1,0,-30*float(self.AG_walk.value("wobble")))
        if "walking" in self.state_test_on(): glRotatef(-8.0*float(self.AG_walk.value("wobble")),0.0,0.0,1.0)

        draw_body=True

        if draw_body:

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
        glScale(1.7,1,.5)
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
        glScale(1.7,1,.5)
        glTranslate(0,-0.5,-2)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["shoe"])
        if drawSolProperly: glutSolidSphere(0.5,24,12)
        glPopMatrix()


        X+=1
        #if (X % 40)==0: self.AG_walk.kick() #ok that works



class Burst:
    
    def __init__(self,life=3,size=0.5,intensity=18,diminish=True,x=0,y=0,z=0,burst_colours=["gold","red","white","red","yellow"],delay=0,callback=None):
        self.life=life
        self.x=x
        self.y=y
        self.z=z
        self.burst_colours=burst_colours
        self.size=size
        self.intensity=intensity
        self.diminish=diminish
        self.delay=delay
        self.callback=callback
        
    def draw(self):
        
        if self.delay>0:
            self.delay-=1
            return False
            
        glDisable(GL_LIGHTING)
        glPushMatrix()
        glTranslate(self.x,self.y,self.z)
        
        for i in range(self.intensity):
            glLineWidth(5.0)
            col = self.burst_colours[random.randint(0,-1+len(self.burst_colours))]
            glColor(colours[col])
            glBegin(GL_LINES)
            #print col            
            glVertex3f(0,0,0)
            glVertex3f(random.uniform(0,self.size*2)-self.size,random.uniform(0,self.size*2)-self.size,random.uniform(0,self.size*2)-self.size)
            glEnd()
            
        glPopMatrix()
        glEnable(GL_LIGHTING)
        self.life-=1
        if self.diminish: self.size-=0.1
        if self.life==0:
            if self.callback!=None: self.callback()
            return True
            
        return False
    
    def createBurst(self,burst_from=[0.0,0.0,0.0], burst_to=[1.0,0.0,0.0], control=None, steps=10, delay=15, callback=None):
        list_of_burst=[]
        if control==None:
            control = [(burst_from[0]+burst_to[0])/2, (burst_from[1]+burst_to[1])/2, (burst_from[2]+burst_to[2])/2]
        for s in range(0,steps+1):
            
            pfrxx=burst_from[0]+(float(s)/steps)*(control[0]-burst_from[0])
            pfryy=burst_from[1]+(float(s)/steps)*(control[1]-burst_from[1])
            pfrzz=burst_from[2]+(float(s)/steps)*(control[2]-burst_from[2])
            
            ptrxx=control[0]+(float(s)/steps)*(burst_to[0]-control[0])
            ptryy=control[1]+(float(s)/steps)*(burst_to[1]-control[1])
            ptrzz=control[2]+(float(s)/steps)*(burst_to[2]-control[2])
            
            pxx = pfrxx + (float(s)/steps)*(ptrxx-pfrxx)
            pyy = pfryy + (float(s)/steps)*(ptryy-pfryy)
            pzz = pfrzz + (float(s)/steps)*(ptrzz-pfrzz)
            
            cb=None
            if s==steps: cb=callback
            
            list_of_burst.append(Burst(x=pxx,y=pyy,z=pzz,delay=s*delay,callback=cb))
        
        return list_of_burst
            
        

class Level:

    grid=None
    baddies=[]
    solomon=None
    sprites=[]
    bursts=[]
    status1 = "status1"
    status2 = "status2"
    status3 = "status3"
    door=None
    target_z=6
    proper_z=6

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
                    self.solomon=Solomon(cc,rr+0.3,self)
                    self.grid[rr][cc]="."
                    self.solomon.A_wandswish.callback=self.block_swap
                    
                elif c=="4":
                    self.door=[cc,rr]
                    self.grid[rr][cc]="."

                elif c=="k":
                    ns=Sprite(cc,rr)
                    ns.setDrawFuncToList(lists["green_key"])
                    ns.collision_action=self.key_detected_something_test
                    self.sprites.append(ns)
                    self.grid[rr][cc]="."


                elif not c in ["b","B","s"]:
                    self.grid[rr][cc]="."

                cc+=1

            rr+=1

        #gotem = Burst().createBurst(burst_from=[-10.0,-10.0,-10.0], steps=30, burst_to=[self.solomon.x,self.solomon.y,0],delay=0.2)
        #print gotem
        #self.bursts=self.bursts + gotem

        self.AG_twinklers=ActionGroup()
        self.AG_twinklers.append("twinkle1",Action(func=self.sin_gen_1,max=200,cycle=True,min=0,reverseloop=False,init_tick=0))
        self.AG_twinklers.append("twinkle2",Action(func=self.sin_gen_2,max=100,cycle=True,min=0,reverseloop=False,init_tick=10))

    def eval_grid(self,coords):
        return self.grid[coords[1]][coords[0]]

    def key_detected_something_test(self):
        print "KEY GOT!"



    def block_swap(self,bump_only=False):

        self.solomon.current_state["wandswish"]=False
        print("hi from block swap "+str(self.solomon))
        takeoff_for_crouching=0
        if self.solomon.state_test(["crouching"])>0 : takeoff_for_crouching=-0.8

        ##if res=="OK": return

        yy = self.block_to_action[1]
        xx = self.block_to_action[0]
        ch = self.grid[yy][xx]
        
        if not bump_only:
            #wand flare!
            crouch=0
            if self.solomon.current_state["crouching"]==True: crouch=-0.4
            self.bursts.append(Burst(x=self.solomon.x+self.solomon.facing*0.5,y=self.solomon.y+crouch,z=0))

        #must be in correct place first
        distanceLeft = (self.solomon.x-1+0.5)-(int(self.solomon.x-1+0.5))
        distanceRight = 1+(int(self.solomon.x+1+0.5))-(self.solomon.x+1+0.5)
        distance = 0
        if self.solomon.facing==-1: distance=distanceLeft
        elif self.solomon.facing==1: distance=distanceRight
            
        #check not in block space when casting
        
        
        if distance > 0.075:
            if bump_only:
                if ch=="b":
                    #print("break block")
                    #self.grid[yy][xx]="B"
                    print("destroy block")
                    self.grid[yy][xx]="B"
                elif ch=="B":
                    print("destroy block")
                    self.grid[yy][xx]="."
                elif ch==".":
                    print("create")
                    self.grid[yy][xx]="b"
            else:
                if ch=="b":
                    #print("break block")
                    #self.grid[yy][xx]="B"
                    print("destroy block")
                    self.grid[yy][xx]="."
                elif ch==".":
                    print("create")
                    self.grid[yy][xx]="b"
                elif ch=="k" and not bump_only:
                    print "*****KEY STRUCK!*****"

    def evaluate(self,joystick,keys):

        self.solomon.stickers=[]

        self.solomon.stickers.append([0,0,0,"white"])
        """ TODO redo current_state was rubbish anyway """
        

        isjumpingoffset=0.3
        #if self.solomon.current_state["jumping"] or self.solomon.current_state["falling"]: isjumpingoffset=0.35
        self.solomon_block_below = [int(self.solomon.x+0.5),int(self.solomon.y-0.1-isjumpingoffset)]
        self.solomon_block_above = [int(self.solomon.x+0.5),int(self.solomon.y+1+0.5)]
        self.solomon_block_above_brow1 = [int(self.solomon.x+0.5+self.solomon.facing*0.2),int(self.solomon.y+1+0.5)]
        self.solomon_block_above_brow2 = [int(self.solomon.x+0.5-self.solomon.facing*0.2),int(self.solomon.y+1+0.5)]
        self.solomon_block_left = [int(self.solomon.x-1+0.5),int(self.solomon.y+0.5)]
        self.solomon_block_right = [int(self.solomon.x+1+0.5),int(self.solomon.y+0.5)]
        self.solomon_block = [int(self.solomon.x+0.5),int(self.solomon.y+0.5)]

        left_grid_is = self.eval_grid(self.solomon_block_left)
        right_grid_is = self.eval_grid(self.solomon_block_right)
        below_grid_is = self.eval_grid(self.solomon_block_below)
        above_brow1_grid_is = self.eval_grid(self.solomon_block_above_brow1)
        above_brow2_grid_is = self.eval_grid(self.solomon_block_above_brow2)

        walktest=False
        #self.status1=""
        #self.status2=""

        if joystick.isDown(keys) and self.solomon.current_state["jumping"]==False:
            self.solomon.current_state["crouching"]=True
            print "crouched"
        else:
            self.solomon.current_state["crouching"]=False

        distanceLeft = (self.solomon.x-1+0.5)-(int(self.solomon.x-1+0.5))
        distanceRight = 1+(int(self.solomon.x+1+0.5))-(self.solomon.x+1+0.5)

        under = self.eval_grid(self.solomon_block_below)
        distance = 1+(int(self.solomon.y+1+0.5))-(self.solomon.y+1+0.5)
        
        #print "dinstance to grid under " + str(distance)
        
        canwalk=False

        if self.solomon.current_state["jumping"]==False and \
            ( under == '.' and ((distanceLeft<0.8 and self.solomon.facing==-1) or (distanceRight<0.8 and self.solomon.facing==1)) ):
            self.solomon.current_state["falling"]=True
            print "falling"
            canwalk=False
        else:
            self.solomon.current_state["falling"]=False
            canwalk=True
            if distance!=0.49 and self.solomon.current_state["jumping"]==False:
                self.solomon.y=round(self.solomon.y)+0.01
                

        if self.solomon.current_state["falling"]==True:
            self.solomon.y-=0.25
            self.solomon.y=round(self.solomon.y,2)
            
        '''
        jumping_counter = 0
        jumping_counter_max = 10
        jump_inc_start = 0.1
        jump_inc = 0.1
        jump_inc_falloff = 0.99
        '''

        floor_solid = below_grid_is in ("b","B","s")
        


        if self.solomon.current_state["jumping"]==False and self.solomon.current_state["crouching"]==False and self.solomon.current_state["falling"]==False and floor_solid:
            if joystick.isUp(keys):
                if self.solomon.jumping_rest==0:
                    self.solomon.jumping_rest=self.solomon.jumping_rest_start
                    self.solomon.current_state["jumping"]=True
                    self.solomon.jumping_counter=0                
                    if joystick.isLeft(keys): self.solomon.jumping_dir=-1
                    elif joystick.isRight(keys): self.solomon.jumping_dir=1
                    else: self.solomon.jumping_dir=0
                    self.solomon.jump_inc = self.solomon.jump_inc_start
                    print "start jump"+str(self.solomon.jumping_dir)
                    print "********************************"
                    dump(self)
                    dump(self.solomon)
                    print "********************************"
                else:
                    self.solomon.jumping_rest-=1
                    

        if self.solomon.current_state["jumping"]==True:
            if self.solomon.jumping_counter>self.solomon.jumping_counter_max:
                self.solomon.current_state["jumping"]=False
                self.solomon.jumping_counter=0
                print "stop jump"
            else:
                self.solomon.jumping_counter+=1
            
        #if self.solomon.jumping_counter>0: print str(self.solomon.jumping_counter)

        if self.solomon.current_state["jumping"]==True:
            if (self.solomon.jumping_dir==1 and (distanceRight>0.4 or right_grid_is==".")) \
            or (self.solomon.jumping_dir==-1 and (distanceLeft>0.4 or left_grid_is==".")):
                self.solomon.x+=self.solomon.jumping_dir*self.solomon.step_inc
                print "jumping and moving jumping dir: {0}, distanceRight {1}, distanceLeft {2}, grid left {3}, grid right {4}".format(self.solomon.jumping_dir,distanceRight,distanceLeft,left_grid_is,right_grid_is)
            self.solomon.y+=round(self.solomon.jump_inc,2)
            self.solomon.jump_inc*=self.solomon.jump_inc_falloff
            
        above = self.eval_grid(self.solomon_block_above)
        distance_above = 1+(int(self.solomon.y-1+0.5))-(self.solomon.y-1+0.5)
        
        #print "dinstance to grid above " + str(distance_above)

        if self.solomon.current_state["jumping"]==True and \
            ( above in [ 'B','b','s' ] and distance_above>0.88): ##and ((distanceLeft<0.8 and self.solomon.facing==-1) or (distanceRight<0.8 and self.solomon.facing==1)) ):
            self.solomon.current_state["jumping"]=False
            print "OUCH"
            if not above=='s':
                self.block_to_action=self.solomon_block_above
                self.block_swap(bump_only=True)
                
        if joystick.isFire(keys):
            if self.solomon.current_state["wandswish"]==False:
                if self.solomon.wand_rest==0:
                    self.solomon.wand_rest=self.solomon.wand_rest_start
                    #start swish
                    self.solomon.current_state["wandswish"]=True   
                    print "swish"
                    if self.solomon.facing==-1: self.block_to_action = self.solomon_block_left
                    elif self.solomon.facing==1: self.block_to_action = self.solomon_block_right
                    if self.solomon.current_state["crouching"]==True:
                        self.block_to_action=[self.block_to_action[0],self.block_to_action[1]-1]
                    
            else:
                #continue swish
                print "blah"
                pass
        
                

        else:
            if joystick.isLeft(keys):
                self.solomon.facing=-1
                self.status1=left_grid_is
                self.status2=str(distanceLeft)+ " L"
                if self.solomon.current_state["jumping"]==False: # and canwalk:
                    if (distanceLeft>0.4 or left_grid_is==".") and self.solomon.current_state["crouching"]==False:
                        self.solomon.x-=self.solomon.step_inc
                        walktest=True

            if joystick.isRight(keys):
                self.solomon.facing=1
                self.status1=right_grid_is
                self.status2=str(distanceRight)+" R"
                if self.solomon.current_state["jumping"]==False: # and canwalk:
                    if (distanceRight>0.4 or right_grid_is==".") and self.solomon.current_state["crouching"]==False:
                        self.solomon.x+=self.solomon.step_inc
                        walktest=True

        #if joystick.isUp(keys):
        #    self.solomon.y+=0.02
        #    walktest=True
        for s in self.sprites:
            dist2 = (s.x-self.solomon.x) * (s.x-self.solomon.x) + (s.y-self.solomon.y) * (s.y-self.solomon.y)
            if dist2 < 0.1:
                s.run_collision_action()
                self.target_z=20
                self.sprites.remove(s)
                gotem = Burst().createBurst(burst_from=[s.x,s.y,0], steps=60, burst_to=[self.door[0],self.door[1],0], control=[self.door[0],self.door[1],5], delay=0.4, callback=self.reset_z)
                #print gotem
                self.bursts=self.bursts + gotem
            
            
        
        floor_solid = below_grid_is in ("b","B","s")
        
        if not floor_solid:
            walktest=False
            self.solomon.current_state["falling"]=True
        
        self.solomon.current_state["walking"] = walktest
        if walktest:
            print "walking"
            self.solomon.AG_walk.do()

        self.solomon.current_state["standing"]
        self.solomon.current_state["crouching"]
        self.solomon.current_state["walking"]
        self.solomon.current_state["jumping"]
        self.solomon.current_state["wandswish"]
        self.solomon.current_state["falling"]

        self.status3=str(self.solomon.y)

        self.AG_twinklers.do()
        
        if self.solomon.wand_rest>0:
            self.solomon.wand_rest-=1
            



    def reset_z(self):
        self.target_z=self.proper_z
        print "reset z called"
        
    def detect(self):
        pass

    def draw(self):

        #global X
        #glRotate(X,1,0,0)

        glPushMatrix()
        glTranslate(8,6.5,-0.55)
        glScale(15,12,0.1)
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["black"])
        glutSolidCube(1)
        glPopMatrix()

        rr=0
        for r in self.grid:
            cc=0
            for c in r:
                #if True:
                if rr>=0 and rr<=13 and cc>=0 and cc<=16:

                    glPushMatrix()
                    glTranslate(cc,rr,0)

                    if c in ["b","s"]:

                        if c=="b": color = [0.3,0.3,1.0,1.0]
                        elif c=="s": color = [1.0,1.0,0.0,1.0]
                        glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
                        #glutWireCube(1)
                        glutSolidCube(1)

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

        if debug==True:

            glPushMatrix()
            glTranslate(self.solomon_block_below[0],self.solomon_block_below[1],0)
            glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["white"])
            glutWireCube(0.85)
            glPopMatrix()

            glPushMatrix()
            glTranslate(self.solomon_block_above[0],self.solomon_block_above[1],0)
            glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["white"])
            glutWireCube(0.85)
            glPopMatrix()
            
            glPushMatrix()
            glTranslate(self.solomon_block_above_brow1[0],self.solomon_block_above_brow1[1],0)
            glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["green"])
            glutWireCube(0.85)
            glPopMatrix()
            
            glPushMatrix()
            glTranslate(self.solomon_block_above_brow2[0],self.solomon_block_above_brow2[1],0)
            glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["green"])
            glutWireCube(0.85)
            glPopMatrix()

            glPushMatrix()
            glTranslate(self.solomon_block_left[0],self.solomon_block_left[1],0)
            glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["white"])
            glutWireCube(0.85)
            glPopMatrix()

            glPushMatrix()
            glTranslate(self.solomon_block_right[0],self.solomon_block_right[1],0)
            glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["white"])
            glutWireCube(0.85)
            glPopMatrix()

        '''
        self.solomon_block_below
        self.solomon_block_above
        self.solomon_block_left
        self.solomon_block_right
        '''

        for s in self.sprites:
            glPushMatrix()
            s.runDetection(self)
            s.draw()
            glPopMatrix()
            s.do()
        
        
        for b in self.bursts:
            if b.draw():
                self.bursts.remove(b)
        
        
            






class SolomonsKey:

    level=None
    keys={}
    cxx,cyy,czz=None,None,None
    tcxx,tcyy,tczz=0,0,0
    fxx,fyy,fzz=None,None,None
    tfxx,tfyy,tfzz=0,0,0

    lastFrameTime=0
    topFPS=0
    camera_sweep = 20
    joystick=Joystick()
    

    def animate(self,FPS=32):

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
        if int(100*time())%100==0:

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

        self.tfxx,self.tfyy,self.tfzz=self.level.solomon.x+0.2*self.level.solomon.facing,self.level.solomon.y-0.5,3.0
        self.tcxx,self.tcyy,self.tczz=self.level.solomon.x+1*self.level.solomon.facing,self.level.solomon.y-0.2,float(self.level.target_z)

        if self.cxx==None: self.cxx=self.tcxx
        if self.cyy==None: self.cyy=self.tcyy
        if self.czz==None: self.czz=self.tczz

        if self.fxx==None: self.fxx=self.tfxx
        if self.fyy==None: self.fyy=self.tfyy
        if self.fzz==None: self.fzz=self.tfzz




        self.cxx+=(self.tcxx-self.cxx)/self.camera_sweep
        self.cyy+=(self.tcyy-self.cyy)/self.camera_sweep
        self.czz+=(self.tczz-self.czz)/self.camera_sweep

        self.fxx+=(self.tfxx-self.fxx)/self.camera_sweep
        self.fyy+=(self.tfyy-self.fyy)/self.camera_sweep
        self.fzz+=(self.tfzz-self.fzz)/self.camera_sweep

        self.lastFrameTime=time()

    def reshape(self,width, height):
        r = float(width) / float(height);
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0,r,1.,50.)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        #glPushMatrix()

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

        #initialization of letters
        self.letters = Letters.Letters()

        #for game models
        MakeLists()

        glutIgnoreKeyRepeat(1)

        glutSpecialFunc(self.keydownevent)
        glutSpecialUpFunc(self.keyupevent)
        glutReshapeFunc(self.reshape)

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
            "sssssssssssssssss",
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
            "sssssssssssssssss"])

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
        )
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
        #print("DISPlAY")





        glLoadIdentity()


        gluLookAt(0, -0.5, 2.5,
                  0, 0, 0  ,
                  0, 1, 0  )


        wdth=0.3
        glTranslate(0.0-(len(self.level.solomon.current_state.keys())-1)*wdth/2.0,-1.3,0)

        if debug==True:
            for k in self.level.solomon.current_state.keys():
                col="red"
                if self.level.solomon.current_state[k]: col="green"
                glMaterialfv(GL_FRONT,GL_DIFFUSE,colours[col])
                glutSolidCube(wdth-0.02)
                glTranslate(wdth,0,0)
                glPushMatrix()
                #glLoadIdentity()
                glScale(0.006,0.01,-0.01)
                glTranslate(-70,4,-20)
                #glTranslate(-180,-70,0)
                glTranslate(wdth,0,0)
                self.letters.drawString(k[:3])
                glPopMatrix()



        glLoadIdentity()


        gluLookAt(0, -0.5, 2.5,
                  0, 0, 0  ,
                  0, 1, 0  )

        wdth=0.2

        joystick_actions=[x for x in dir(self.joystick) if x[0:2]=="is"]
        glTranslate(0.0-(len(joystick_actions)-1)*wdth/2.0,-1.0,0)

        if debug==True:
            for k in joystick_actions:
                #print(k)
                col="red"
                if getattr(self.joystick,k)(self.keys): col="green"
                glMaterialfv(GL_FRONT,GL_DIFFUSE,colours[col])
                glutSolidCube(wdth-0.02)
                glTranslate(wdth,0,0)



        glLoadIdentity()

        #26 characters centred:

        #self.status1 = ""
        #self.status2 = ""


        gluLookAt(0, 0, 2.5,
                  0, 0, 0  ,
                  0, 1, 0  )

        glScale(0.01,0.01,-0.01)
        glTranslate(-180,-70,0)

        if debug==True:
            self.letters.drawString(self.level.status1)
            glTranslate(0,0-15,0)
            self.letters.drawString(self.level.status2)
            glTranslate(0,0-15,0)
            self.letters.drawString(self.level.status3)

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