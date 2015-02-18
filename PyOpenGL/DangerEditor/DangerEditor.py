from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import random 
import sys
from time import time
#import math
from Letters import lists, MakeLists

import re

name = "thing"

colours={}

colours["black"]=[0.1,0.1,0.1,1.0]
colours["gold"]=[1.0,0.9,0.0,1.0]
colours["red"]=[1.0,0.0,0.0,1.0]
colours["green"]=[0.0,1.0,0.0,1.0]
colours["blue"]=[0.0,0.0,1.0,1.0]
colours["yellow"]=[1.0,1.0,0.0,1.0]
colours["cyan"]=[0.0,1.0,1.0,1.0]
colours["pink"]=[1.0,0.0,1.0,1.0]
colours["white"]=[1.0,1.0,1.0,1.0]
  
file_name=sys.argv[0]
if file_name=="":
    file_name="DangerCode"+str(strftime("%Y%m%d_%H%M%S"))+".txt"




'''

browse:

list of push-pops

up/down scroll
right - select > list transforms etc
esc - list of push-pops



a - add > list
    cube
    sphere
    cone
    
    > name it
'''

class Joystick:
    
    keys={}
    up,down,left,right,fire="","","","",""
    isPressed=False
    

    def __init__(self,up=101,down=103,left=100,right=102,fire="m"):

        self.isAlt=False
        self.isShift=False     
        self.isControl=False
        self.up=up
        self.down=down
        self.left=left
        self.right=right
        self.fire=fire
        self.fire=fire
        self.keys[self.up]=False
        self.keys[self.down]=False
        self.keys[self.left]=False
        self.keys[self.right]=False
        self.keys[self.fire]=False   

    def register(self,ch,down):
        #print "register "+str(ch)+str(type(ch))
        extra=""
        if type(ch) is str:
            extra=str(ord(ch))
            if extra in ["13","27","8"]: ch=int(extra)
            
        #if not self.keys.has_key(ch): print str(ch)+" "+extra
        self.keys[ch]=down
        
    def isKey(self,ch):
        if self.keys.has_key(ch): 
            return self.keys[ch]
        else: return False        
        
    def isUp(self):
        if self.keys.has_key(self.up): 
            return self.keys[self.up]
        else: return False
         
    def isDown(self):
        if self.keys.has_key(self.down): return self.keys[self.down]
        else: return False
         
    def isLeft(self):
        if self.keys.has_key(self.left): return self.keys[self.left]
        else: return False
         
    def isRight(self):
        if self.keys.has_key(self.right): return self.keys[self.right]
        else: return False
         
    def isFire(self):
        if self.keys.has_key(self.fire): return self.keys[self.fire]
        else: return False
           
  
class Thing:

    lastFrameTime=0

    state="browse"
    
    xx,yy,zz=0,0,5
    cxx,cyy,czz=0,0,0
    X=0
    
    xRot=0
    yRot=0
    mPos=[0,0]
    speed=0.1
    
    menu=[]
    menuindex=0
    
    temp=[]
    editing=None
    edititem=None

    joystick=Joystick()

    def animate(self,FPS=1):
    
        
        
        currentTime=time()
        
        
        
        
        if self.state=="browse":

            if self.joystick.isKey("a"):
                self.state="add"
                self.menu=["CUBE","SPHERE","CONE","DISC","ROTATE","TRANSLATE","SCALE","COLOR"]
                self.edititem=self.menuindex
                self.menuindex=0
                
            if self.joystick.isKey("u"):
                if len(self.temp)>1: self.temp.insert((self.menuindex-1)%(len(self.temp)),self.temp.pop(self.menuindex))
                if len(self.menu)>0: self.menuindex=( self.menuindex-1 ) % len(self.menu)
                
            elif self.joystick.isKey("d"):
                if len(self.temp)>1: self.temp.insert((self.menuindex+1)%(len(self.temp)),self.temp.pop(self.menuindex))
                if len(self.menu)>0: self.menuindex=( self.menuindex+1 ) % len(self.menu)
                
            elif self.joystick.isKey(13) and len(self.temp)>0:  
                if self.joystick.isControl==True:
                    f.open(fille_name,"w")
                    for ll in self.temp:
                        f.write(ll+"\n")
                    f.write("\n")
                    f.close()
                    print "written out file "+str(file_name)
          
                else:
                    self.state="edit"
                    
                    if self.menuindex<len(self.menu): self.editing=self.menu[self.menuindex]
                    else: self.menuindex=0
                    
                    self.edititem=self.menuindex
                    commands=self.editing.split("###")[1:]
                    if len(commands)>0:
                        values=re.findall("-{0,1}[0-9\.]+",self.editing)
                        print "commands "+str(commands)
                        print "values "+str(values)
                        self.menu=[str(k)+" "+str(v) for k,v in zip(commands,values)]
                        self.menuindex=0
                    else:         
                        self.state="browse"
                    
            
            elif self.joystick.isKey(8) and len(self.temp)>0:            
                print "delete!"
                self.temp.pop(self.menuindex)
                if self.menuindex>=len(self.temp): self.menuindex=len(self.temp)-1
            
            
            
        if self.joystick.isUp():
            print "menu length: "+str(len(self.menu))
            if len(self.menu)>0: self.menuindex=( self.menuindex-1 ) % len(self.menu)
            print self.menuindex
            
            
        if self.joystick.isDown():
            print "menu length: "+str(len(self.menu))
            if len(self.menu)>0: self.menuindex=( self.menuindex+1 ) % len(self.menu)
            print self.menuindex
            
        if self.joystick.isKey(13):
        
            if self.state=="add":
            
                if self.menu[self.menuindex]=="CUBE":
                    self.temp.insert(self.edititem,"glutSolidCube(0.5) ###size")  #+="glPushMatrix()\nglutSolidCube(0.5)\nglPopMatrix()\n"
                    self.state="browse"
                    #self.menuindex=0
                elif self.menu[self.menuindex]=="SPHERE":
                    self.temp.insert(self.edititem,"glutSolidSphere(0.5,12,12) ###size###segments###stacks")  
                    self.state="browse"
                    #self.menuindex=0
                elif self.menu[self.menuindex]=="CONE":                    
                    ##note there are two item to add so this is back to front
                    self.temp.insert(self.edititem,"glutSolidCone(0.5,0.5,12,1) ###radius###size###segs###stacks")   
                    self.temp.insert(self.edititem,"q=gluNewQuadric()")                        
                    ####self.temp.insert(self.edititem,"glutSolidSphere(0.5,12,12) ###size###segments###stacks")  
                    self.state="browse"
                    #self.menuindex=0
                elif self.menu[self.menuindex]=="DISC":
                    ##note there are two item to add so this is back to front
                    self.temp.insert(self.edititem,"gluDisk(q,0.05,0.2,12,12) ###xxx###yyy###segments###stacks")  
                    self.temp.insert(self.edititem,"q=gluNewQuadric()")
                    ####self.temp.insert(self.edititem,"glutSolidSphere(0.5,12,12) ###size###segments###stacks")  
                    self.state="browse"
                    #self.menuindex=0
                elif self.menu[self.menuindex]=="COLOR":
                    self.temp.insert(self.edititem,"glColor(0.0,0.0,0.0) ###col_r###col_g###col_b")   
                    self.state="browse"
                    #self.menuindex=0
                elif self.menu[self.menuindex]=="ROTATE":
                    self.temp.insert(self.edititem,"glRotate(0.0,0,1,0) ###value###axis_x###axis_y###axis_z")  
                    self.state="browse"
                    #self.menuindex=0
                elif self.menu[self.menuindex]=="TRANSLATE":
                    self.temp.insert(self.edititem,"glTranslate(0.0,0.0,0.0) ###trans_x###trans_y###trans_z")   
                    self.state="browse"
                    #self.menuindex=0
                elif self.menu[self.menuindex]=="SCALE":
                    self.temp.insert(self.edititem,"glScale(1.0,1.0,1.0) ###scale_x###scale_y###scale_z")    
                    self.state="browse"
                    #self.menuindex=0
            
        

        if self.state=="edit":
            if self.joystick.isLeft():
                print "editting"
                print str(self.editing)
                print str(self.edititem)
                print str(self.menuindex)
                print "left"                
                
                if self.edititem>=len(self.menu): self.edititem=0

                commands=self.editing.split("###")[1:]
                if len(commands)>0:
                    values=re.findall("-{0,1}[0-9\.]+",self.editing)
                  
                editing_command=commands[self.menuindex]
                editing_value=float(values[self.menuindex])
                    
                val=0.1
                if self.joystick.isShift: val=1
                elif self.joystick.isControl: val=0.01
                editing_value-=val
                
                old=self.editing
                m=None
                mit=re.finditer("-{0,1}[0-9\.]+",old)
                for i in range(0,self.menuindex+1):
                    m=mit.next()
                    
                #print "m: "+str(m)+" "+str(dir(m))+" "+str(m.group())+" ms:"+str(m.start())+ "me:"+str(m.end())
                
                neww=old[0:m.start()]+str(editing_value)+old[m.end():]
                
                self.temp[self.edititem]=neww
                self.menu[self.edititem]=str(editing_command)+" "+str(editing_value)
                self.editing=neww        
                
            
            if self.joystick.isRight():
                print "editting"
                print str(self.editing)
                print str(self.edititem)
                print str(self.menuindex)
                print "right"
                
                commands=self.editing.split("###")[1:]
                if len(commands)>0:
                    values=re.findall("-{0,1}[0-9\.]+",self.editing)
                  
                editing_command=commands[self.menuindex]
                editing_value=float(values[self.menuindex])
                    
                val=0.1
                if self.joystick.isShift: val=1
                elif self.joystick.isControl: val=0.01

                editing_value+=val                  
                
                old=self.editing
                m=None
                mit=re.finditer("-{0,1}[0-9\.]+",old)
                for i in range(0,self.menuindex+1):
                    m=mit.next()
                    
                #print "m: "+str(m)+" "+str(dir(m))+" "+str(m.group())+" ms:"+str(m.start())+ "me:"+str(m.end())
                
                neww=old[0:m.start()]+str(editing_value)+old[m.end():]
                
                self.temp[self.edititem]=neww
                self.menu[self.edititem]=str(editing_command)+" "+str(editing_value)
                self.editing=neww
                
            
        
            
        if self.joystick.isKey(27): self.state="browse"
            
        
        
        
        
        
        
        
        self.X+=1
        if self.X>1000: self.X=0
               
        #print "posting redisplay"
        glutPostRedisplay()    
        
        tt=int(1000/FPS)
        #print tt, FPS
        glutTimerFunc(tt, self.animate, FPS)
        drawTime=currentTime-self.lastFrameTime
        self.topFPS=int(1000/drawTime)
        if int(100*time())%100==0: print "draw time "+str(drawTime)+" top FPS "+str(1000/drawTime)+str((self.temp))
        
        
        
        
        
    def draw(self):
                
           
        glPushMatrix()
        glTranslate(0,0,3)
        glRotate(-self.yRot*2,1,0,0)
        glRotate(-self.xRot*2,0,1,0)                                
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["white"])
        glutWireCube(1)
        
        
        '''
        f=open(file_name,"r")
        code=f.read()
        exec(code)
        '''
        for t in self.temp: exec(t)
        
        
        
        glPopMatrix()
        
        #string=""
        #if self.joystick.isUp(): string="UP"
        #elif self.joystick.isDown(): string="DOWN"
        #elif self.joystick.isLeft(): string="LEFT"
        #elif self.joystick.isRight(): string="RIGHT"
        #elif self.joystick.isFire(): string="FIRE"
        
        
        glDisable(GL_LIGHTING)
        
        glPushMatrix()  
        glTranslate(-0.7,0,0)
        glScale(0.003,0.003,0.003)
        glTranslate(0,0,1295)
        glTranslate(20,0,0)
        mn=0
        
        
        self.drawString(self.state.upper())
        glTranslate(0,-11,0)
        
        temponly=False
                
        
        if self.state=="browse":
            if len(self.menu)==0:
                self.menu=["NO ITEMS"]
                temponly=True
            else:
                self.menu=self.temp        
        
        
        for mi in self.menu:
            string=mi
            #print mi
            if mn==self.menuindex:
                #print "yo!"
                string="*"+mi
            #glTranslate(10,0,0)
            glTranslate(0,-14,0)
            self.drawString(string)
            mn+=1
                
                
        if temponly==True: self.menu=[]
          
        glPopMatrix()
        
        glEnable(GL_LIGHTING)



    def drawString(self,string):
        glPushMatrix()
        for l in range(0,len(string)):
            if string[l].upper()=="#": break
            glTranslate(14,0,0)
            
            
            
            glPushMatrix()
            glColor(colours["black"])
            glLineWidth(5.0)
            if lists.has_key(string[l].upper()): glCallList(lists[string[l].upper()])  
            else:  glCallList(lists[" "])              
            glPopMatrix()
            
            
            glPushMatrix()
            glTranslate(0,0,1)
            glColor(colours["white"])
            glLineWidth(0.5)
            if lists.has_key(string[l].upper()): glCallList(lists[string[l].upper()])  
            else:  glCallList(lists[" "])            
            glPopMatrix()
            
            
            
        glPopMatrix()


    def __init__(self):   
     
             
        MakeLists()
    
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
        
        self.animate(FPS=10)
        
        MakeLists()
        glutMainLoop()
        
        
        return

    def keydownevent(self,c,x,y):    

        mod = glutGetModifiers()

        self.joystick.isControl=False
        self.joystick.isAlt=False
        self.joystick.isShift=False

        if mod&GLUT_ACTIVE_CTRL==GLUT_ACTIVE_CTRL: self.joystick.isControl=True
        if mod&GLUT_ACTIVE_ALT==GLUT_ACTIVE_ALT: self.joystick.isAlt=True
        if mod&GLUT_ACTIVE_SHIFT==GLUT_ACTIVE_SHIFT: self.joystick.isShift=True

        print str(c)
        if type(c) is str: self.joystick.register(c.lower(),True)
        else: self.joystick.register(c,True)
        glutPostRedisplay()
        
    def keyupevent(self,c,x,y):  

        mod = glutGetModifiers()

        self.joystick.isControl=False
        self.joystick.isAlt=False
        self.joystick.isShift=False

        if mod&GLUT_ACTIVE_CTRL==GLUT_ACTIVE_CTRL: self.joystick.isControl=True
        if mod&GLUT_ACTIVE_CTRL==GLUT_ACTIVE_ALT: self.joystick.isAlt=True
        if mod&GLUT_ACTIVE_CTRL==GLUT_ACTIVE_SHIFT: self.joystick.isShift=True

        if type(c) is str: self.joystick.register(c.lower(),False)
        else: self.joystick.register(c,False)
        glutPostRedisplay()
        
    def mousedrag(self,x,y):
        #print ((x,y))
        self.xRot+=(self.mPos[0]-x)*self.speed
        self.yRot+=(self.mPos[1]-y)*self.speed
        self.mPos=[x,y]

    def mouse(self,button,state,x,y):
        #print ((button,state,x,y))
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
        #self.yRot+=0.5
        #self.xRot+=0.5
    
    
        glutSwapBuffers()
        #return


"""
Do this because if it gets put through pydoc or imported its automatically executed
"""
if __name__ == '__main__': Thing()
