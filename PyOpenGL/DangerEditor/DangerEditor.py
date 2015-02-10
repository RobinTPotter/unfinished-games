from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import random 
import sys
from time import time
#import math
from Letters import lists, MakeLists

name = "thing"

colours={}

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

temp=""



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

    def __init__(self,up=101,down=103,left=100,right=102,fire="m"):
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
        print "register "+str(ch)+str(type(ch))
        extra=""
        if type(ch) is str:
            extra=str(ord(ch))
            if extra=="13": ch=13
            
        if not self.keys.has_key(ch): print str(ch)+" "+extra
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

    joystick=Joystick()

    def animate(self,FPS=1):
        
        global temp
        
        currentTime=time()
        
        
        if self.state=="browse" and self.joystick.isKey("a"):
            self.state="add"
            self.menu=["CUBE","SPHERE","CONE","DISC"]
            self.menuindex=0
            
            
            
        if self.joystick.isUp():
            self.menuindex-=1
            if self.menuindex<0: self.menuindex=0
            
        if self.joystick.isDown():
            self.menuindex+=1
            if self.menuindex>(len(self.menu)-1): self.menuindex=len(self.menu)-1
            
        if self.state=="add" and self.joystick.isKey(13):
            print "bello"
            if self.menu[self.menuindex]=="CUBE": temp+="glPushMatrix()\nglutSolidCube(1)\nglPopMatrix()\n"
            elif self.menu[self.menuindex]=="SPHERE": temp+="glPushMatrix()\nglutSolidSphere(1,8,8)\nglPopMatrix()\n"
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        self.X+=1
        if self.X>1000: self.X=0
               
        #print "posting redisplay"
        glutPostRedisplay()    
        
        tt=int(1000/FPS)
        #print tt, FPS
        glutTimerFunc(tt, self.animate, FPS)
        drawTime=currentTime-self.lastFrameTime
        self.topFPS=int(1000/drawTime)
        if int(100*time())%100==0: print "draw time "+str(drawTime)+" top FPS "+str(1000/drawTime)
        
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
        exec(temp)
        
        
        
        glPopMatrix()
        
        #string=""
        #if self.joystick.isUp(): string="UP"
        #elif self.joystick.isDown(): string="DOWN"
        #elif self.joystick.isLeft(): string="LEFT"
        #elif self.joystick.isRight(): string="RIGHT"
        #elif self.joystick.isFire(): string="FIRE"
        
        
        glDisable(GL_LIGHTING)
        glPushMatrix()  
        glLineWidth(2.0)
        glTranslate(0,0,3.8)
        glScale(0.003,0.003,0.003)
        glTranslate(100,0,0)
        mn=0
        
        
        self.drawString(self.state.upper())
        glTranslate(0,-11,0)
        
        if len(self.menu)==0:
            self.drawString("NO ITEMS")
        else:
            for mi in self.menu:
                string=mi
                #print mi
                if mn==self.menuindex:
                    #print "yo!"
                    string="*"+mi
                #glTranslate(10,0,0)
                glTranslate(0,-11,0)
                self.drawString(string)
                mn+=1
                
        glPopMatrix()
        glEnable(GL_LIGHTING)



    def drawString(self,string):
        glPushMatrix()
        glMaterialfv(GL_FRONT,GL_DIFFUSE,colours["white"])
        for l in range(0,len(string)):
            glTranslate(11,0,0)
            glCallList(lists[string[l].upper()])  
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
        if type(c) is str: self.joystick.register(c.lower(),True)
        else: self.joystick.register(c,True)
        
        glutPostRedisplay()
        
    def keyupevent(self,c,x,y):    
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
