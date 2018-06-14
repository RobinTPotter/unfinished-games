from charSolomon import Solomon
from Action import Action, ActionGroup
from charBurst import Burst
from Joystick import Joystick
from Sprite import Sprite
from Models import lists, MakeLists, colours
from math import sin, cos, pi, floor, ceil, sqrt
from OpenGL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from config import *

def generateLevel(num):
    if num==0:
        return Level(["sssssssssssssssss",
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

    if num==1:
        return Level([
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
            "sssssssssssssssss"])


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

        if joystick.isDown(keys) and self.solomon.current_state["jumping"]==False:
            self.solomon.current_state["crouching"]=True
            print "crouched"
        else:
            self.solomon.current_state["crouching"]=False

        distanceLeft = (self.solomon.x-1+0.5)-(int(self.solomon.x-1+0.5))
        distanceRight = 1+(int(self.solomon.x+1+0.5))-(self.solomon.x+1+0.5)

        under = self.eval_grid(self.solomon_block_below)
        distance = 1+(int(self.solomon.y+1+0.5))-(self.solomon.y+1+0.5)
        
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
                else:
                    self.solomon.jumping_rest-=1

        if self.solomon.current_state["jumping"]==True:
            if self.solomon.jumping_counter>self.solomon.jumping_counter_max:
                self.solomon.current_state["jumping"]=False
                self.solomon.jumping_counter=0
                print "stop jump"
            else:
                self.solomon.jumping_counter+=1
            
        if self.solomon.current_state["jumping"]==True:
            if (self.solomon.jumping_dir==1 and (distanceRight>0.4 or right_grid_is==".")) \
            or (self.solomon.jumping_dir==-1 and (distanceLeft>0.4 or left_grid_is==".")):
                self.solomon.x+=self.solomon.jumping_dir*self.solomon.step_inc
                print "jumping and moving jumping dir: {0}, distanceRight {1}, distanceLeft {2}, grid left {3}, grid right {4}".format(self.solomon.jumping_dir,distanceRight,distanceLeft,left_grid_is,right_grid_is)
            self.solomon.y+=round(self.solomon.jump_inc,2)
            self.solomon.jump_inc*=self.solomon.jump_inc_falloff
            
        above = self.eval_grid(self.solomon_block_above)
        distance_above = 1+(int(self.solomon.y-1+0.5))-(self.solomon.y-1+0.5)
        
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

        for s in self.sprites:
            glPushMatrix()
            s.runDetection(self)
            s.draw()
            glPopMatrix()
            s.do()
        
        for b in self.bursts:
            if b.draw():
                self.bursts.remove(b)
        
        
            




