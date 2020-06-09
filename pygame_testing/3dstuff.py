#! /usr/bin/python3
import sys
import pygame as pg
import threading
import argparse
from math import sin, cos, pi

SIZE = (640, 480)
DEBUG=True


class Matrix:
    def __init__(self, x,y,z,t):
        self.x=x
        self.y=y
        self.z=z
        self.t=t

class Point():
    def __init__(self, x=0, y=0, z=0, *args):
        self.x=x
        self.y=y
        self.z=z

        if isinstance(args, (tuple)) and len(args)==3:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]

        if isinstance(args, (tuple)) and len(args)==2:
            self.x = args[0]
            self.y = args[1]
    
    def __add__(self, point):
        if isinstance(point,Point):
            return Point(self.x+point.x,self.y+point.y,self.z+point.z)
        elif isinstance(point,(int,float)):
            return Point(self.x+point,self.y+point,self.z+point)
        else:
            print('operation not allowed add {} to {}'.format(self, point))
            return None

    def __mul__(self, point):
        if isinstance(point,Point):
            return Point(self.x*point.x,self.y*point.y,self.z*point.z)
        elif isinstance(point,(int,float)):
            return Point(self.x*point,self.y*point,self.z*point)
        else:
            print('operation not allowed mult {} to {}'.format(self, point))
            return None
            
    def __truediv__(self, point):
        if isinstance(point,Point):
            return Point(self.x/point.x,self.y/point.y,self.z/point.z)
        elif isinstance(point,(int,float)):
            return Point(self.x/point,self.y/point,self.z/point)
        else:
            print('operation not allowed truediv {} to {}'.format(self, point))
            return None
    
    def matrix_mult(self,matrix):
        return Point( 
            self.x * matrix.x.x+self.y*matrix.x.y+self.z*matrix.x.z+matrix.t.x,
            self.x*matrix.y.x+self.y*matrix.y.y+self.z*matrix.y.z+matrix.t.y,
            self.x*matrix.z.x+self.y*matrix.z.y+self.z*matrix.z.z+matrix.t.z
        )
    def tup(self):
        return (self.x, self.y, self.z)

    def project(self,dim):
        if self.z>0: return dim[0]/2 + self.x/self.z,dim[1]/2 + self.y/self.z
        else: return None
        

from random import randint

class Colours():
    blue = (0, 0, 255)
    red = (255, 0, 0)
    darkRed = (128, 0, 0)
    green = (0, 255, 0)
    darkGreen = (0, 128, 0)
    darkBlue = (0, 0, 64)
    white = (255, 255, 255)
    darkGrey = (64, 64, 64)
    grey = (128, 128, 128)
    black = (0, 0, 0)
    pink = (255, 200, 200)
    
def var(c):
    return (
        min(c[0] + randint(0,20),255),
        min(c[1] + randint(0,20),255),
        min(c[2] + randint(0,20),255)  
    )



camera = Matrix(Point(1,0,0),Point(0,1,0),Point(0,0,1),Point(0,0,0.011))

class Polygon:
    def __init__(self,tup):
        self.points = []
        for p in range(0,int(tup[0])):
            pp=p*3
            self.points.append(  Point(  float(tup[pp+1]) , float(tup[pp+2]) , 0.00001+float(tup[pp+3])     )   )

    def matrix_mult_project(self,matrix,SIZE):
        mm = [p.matrix_mult(matrix) for p in self.points]
        pr = [p.project(SIZE) for p in mm if p.z>0]
        if len(pr)>=3:
            pp = [p for p in pr if p[0]>-50 and p[0]<SIZE[0]+50 and p[1]>-50 and p[1]<SIZE[1]+50]
            if len(pp)>=3:
                return pp
    

class Gogo():
    def __init__(self, size=(720, 480)):
        self.clock = pg.time.Clock()
        self.working = True
        with open('output.poly') as fl:
            data = fl.readlines()
            data = [d.split(',') for d in data]
            self.model = [Polygon(d) for d in data]

        print(self.model) 
        self.thread = threading.Thread(target=self.gogo)
        if DEBUG: print('starting thread')
        self.thread.start()
   
    def get_working(self):
        return self.working

    def tf(self,point):
        from random import randint
        me = Point(point.x, point.y)+Point(randint(-1,1),randint(-1,1))/2
        return me

    def gogo(self):
        print('gogo')
        pg.init()
        self.screen = pg.display.set_mode(SIZE)
        while self.get_working():
            camera.t.x -= 0.01
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.working = False

            self.screen.fill(Colours.darkBlue)
            for pol in self.model:
                ply = pol.matrix_mult_project(camera, SIZE)
                if ply is not None: pg.draw.polygon(self.screen, Colours.darkGreen, ply)
                #for p in range(len(pol.points)):
                #    l1 = pol.points[p].matrix_mult(camera).project(SIZE)
                #    l2 = pol.points[(p+1) % len(pol.points)].matrix_mult(camera).project(SIZE)
                #    if l1 is not None and l2 is not None: 
                #        #print (l1,l2)
                #        pg.draw.line(self.screen, Colours.white, l1, l2, 1)

            
            pg.display.flip()
        
        pg.display.quit()
        if DEBUG: print('end')
        return

if __name__=='__main__':
    print('boo')
    DEBUG=False
    g=Gogo(SIZE)
