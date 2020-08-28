#! /usr/bin/python3
import sys
import pygame as pg
import threading
import argparse
from math import sin, cos, pi

SIZE = (640, 480)
DEBUG=True

import numpy as np
from numpy import matlib as m

class Camera:
    def __init__(self, **kwargs):
        self._matrix = m.identity(4)
        self.setU(Point(1,0,0))
        self.setV(Point(0,1,0))
        self.setD(Point(0,0,1))
        self.setPos(Point(0,0,0))
        #self._matrix.itemset(15,  0)
    def __repr__(self):
        return '{}'.format(self._matrix)
    def setU(self, u):
        u.normalize()
        self._u = u
        self._matrix.itemset(0, u.x())
        self._matrix.itemset(4, u.y())
        self._matrix.itemset(8, u.z())
        self.update()
    def setV(self, v):
        v.normalize()
        self._v = v
        self._matrix.itemset(1, v.x())
        self._matrix.itemset(5, v.y())
        self._matrix.itemset(9, v.z())
        self.update()
    def setD(self, d):
        d.normalize()
        self._d = d
        self._matrix.itemset(2,  d.x())
        self._matrix.itemset(6,  d.y())
        self._matrix.itemset(10, d.z())
        self.update()
    def setPos(self, p):
        self._p = p
        self._matrix.itemset(12,  p.x())
        self._matrix.itemset(13,  p.y())
        self._matrix.itemset(14,  p.z())
        self.update()
    def getPos(self):
        return self._p
        
    def update(self):
        self._inv = np.linalg.inv(self._matrix)
        
    def rotateU(self, angle):
        cur = self._u
        dd = self._d.rotate(cur, angle)
        vv = self._v.rotate(cur, angle)
        #print(uu)
        self.setD(dd)
        self.setV(vv)
    def rotateV(self, angle):
        cur = self._v
        uu = self._u.rotate(cur, angle)
        dd = self._d.rotate(cur, angle)
        #print(uu)
        self.setU(uu)
        self.setD(dd)
    def rotateD(self, angle):
        cur = self._d
        uu = self._u.rotate(cur, angle)
        vv = self._v.rotate(cur, angle)
        #print(uu)
        self.setU(uu)
        self.setV(vv)
        

class Point:
    def __init__(self,x=0,y=0,z=0):
        self._vector = np.array([x,y,z,1])
    def __repr__(self):
        return '(x={},y={},z={})'.format(self.x(),self.y(),self.z())
    def normalize(self):
        norm = np.linalg.norm(self._vector[:3])
        if norm != 0: 
           self._vector = self._vector / norm
        #print(norm)
        #sys.exit(0)
        return self._vector
    def x(self):
        return self._vector[0]
    def y(self):
        return self._vector[1]
    def z(self):
        return self._vector[2]
    def matrix_mult(self,matrix):
        hello = np.asarray(self._vector*matrix)
        return Point( 
            hello[0][0],hello[0][1],hello[0][2]
        )
    def project(self,dim):
        if self.z()>0: return dim[0]/2 + self.x()/self.z(),dim[1]/2 + self.y()/self.z()
        else: return None
    def rotate(self, axis, angle):
        if self.x() == 0 and self.y() == 0 and self.z() == 0: return
        w = Point()
        axis.normalize()
        c = cos(angle)
        s = sin(angle)
        t = 1 - c
        w = Point( (t * axis.x() * axis.x() + c) * self.x()  + (t * axis.x() * axis.y() + s * axis.z()) * self.y()	+ (t * axis.x() * axis.z() - s * axis.y()) * self.z()
        , (t * axis.x() * axis.y() - s * axis.z()) * self.x()  + (t * axis.y() * axis.y() + c) * self.y() 	+ (t * axis.y() * axis.z() + s * axis.x()) * self.z()
        , (t * axis.x() * axis.z() + s * axis.y()) * self.x()  + (t * axis.y() * axis.z() - s * axis.x()) * self.y() + (t * axis.z() * axis.z() + c) * self.z()
        )
        w.normalize()
        return w
        
    def __add__(self, p):
        n = Point()
        n._vector = self._vector + p._vector
        return n


class Polygon:
    def __init__(self,**kwargs):
        if 'radius' in kwargs and 'num' in kwargs:
            radius = kwargs['radius']
            num = kwargs['num']
            self.points = []
            for p in range(kwargs['num']):
                self.points.append(Point(round(radius * cos(2*pi*p/num),6),  round(radius * sin(2*pi*p/num),6) , 0 ) )
        elif 'data' in kwargs and 'num' in kwargs:        
            self.points = []
            data = kwargs['data']
            num = kwargs['num']
            pd = [aa for aa in zip(data[0:len(data):3], data[1:len(data):3], data[2:len(data):3])]
            for p in range(num):
                pl = Point(float(pd[p][0]),float(pd[p][1]),float(pd[p][2]))
                self.points.append(pl)
        else:
            self.points = Polygon(radius=1, num=4).points
    def __repr__(self):
        return 'Polygon {}'.format(self.points)
    def matrix_mult_project(self, camera, size, orientation=Camera()):
        self.shape = []
        points = [(p).matrix_mult(camera._inv) for p in self.points]
        
        mm = [(p).matrix_mult(orientation._inv) for p in points]
        #print(mm)
        pr = [p.project(size) for p in mm if p.z()>0]
        if len(pr)>=3:
            pp = [p for p in pr if p[0]>-50 and p[0]<SIZE[0]+50 and p[1]>-50 and p[1]<SIZE[1]+50]
            if len(pp)>=3:
                return pp


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
    





class Model:

    def __init__(self,polys):
        self.polygons = polys
        self.orientation = Camera()
        self.orientation.setPos(Point(0,0,-0.1))
        
    def draw(self, screen, camera, size):
        for pol in self.polygons:
            ply = pol.matrix_mult_project(camera, size, orientation=self.orientation)
            #print(ply)
            if ply is not None:
                pg.draw.polygon(screen, Colours.darkGreen, ply)



class Gogo():
    def __init__(self, size=(720, 480)):
        self.clock = pg.time.Clock()
        self.working = True
        with open('output.poly') as fl:
            data = fl.readlines()
            data = [d.split(',') for d in data]
            self.model = Model([Polygon(num=int(d[0]), data=d[1:]) for d in data])
            self.model.pos = Point(0,0,0.1)
        
        #self.model = [Polygon(radius=-3040, num=3)]
      
        self.init_controls()
      
        print(self.model) 
        self.thread = threading.Thread(target=self.gogo)
        self.camera = Camera()
        self.camera.setPos(Point(2,0,0))
        print(self.camera) 
        if DEBUG: print('starting thread')
        self.thread.start()
   
    def init_controls(self):
        control = type('control', (object,), { "key": 0, "status": False } )
        self.controls = type('controls', (object,), { "left": control(), "right": control(), "up": control(), "down": control(), "go": control() })        
        self.controls.left.key = pg.K_LEFT
        self.controls.right.key = pg.K_RIGHT       
        self.controls.up.key = pg.K_UP
        self.controls.down.key = pg.K_DOWN
        self.controls.go.key = pg.K_SPACE
        
   
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
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.working = False
                    
                if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                    if event.key == self.controls.left.key:
                        self.controls.left.status = event.type == pg.KEYDOWN 
                    if event.key == self.controls.right.key:
                        self.controls.right.status = event.type == pg.KEYDOWN 
                    if event.key == self.controls.down.key:
                        self.controls.down.status = event.type == pg.KEYDOWN 
                    if event.key == self.controls.up.key:
                        self.controls.up.status = event.type == pg.KEYDOWN 
                    if event.key == self.controls.go.key:
                        self.controls.go.status = event.type == pg.KEYDOWN 
                        

            self.screen.fill(Colours.darkBlue)
            self.model.orientation.rotateD(0.05)
            self.model.draw(self.screen, self.camera, SIZE)
                #for p in range(len(pol.points)):
                #    l1 = pol.points[p].matrix_mult(camera).project(SIZE)
                #    l2 = pol.points[(p+1) % len(pol.points)].matrix_mult(camera).project(SIZE)
                #    if l1 is not None and l2 is not None: 
                #        #print (l1,l2)
                #        pg.draw.line(self.screen, Colours.white, l1, l2, 1)

            #if self.controls.left.status or self.controls.right.status:
            #    p = self.camera.getPos()                
            #    if self.controls.right.status: p._vector[0] += 1
            #    if self.controls.left.status: p._vector[0] -= 1
            #    self.camera.setPos(p)
            #
            #if self.controls.up.status or self.controls.down.status:
            #    p = self.camera.getPos()                
            #    if self.controls.up.status: p._vector[1] += 1
            #    if self.controls.down.status: p._vector[1] -= 1
            #    self.camera.setPos(p)
            #
            #if self.controls.go.status: self.camera.rotateV(0.2)
            
            if self.controls.left.status or self.controls.right.status:
                if self.controls.left.status: self.camera.rotateV(0.02)
                elif self.controls.right.status: self.camera.rotateV(-0.02)
            
            if self.controls.up.status or self.controls.down.status:
                if self.controls.up.status: self.camera.rotateU(0.02)
                elif self.controls.down.status: self.camera.rotateU(-0.02)
            
            print(self.camera._inv)
            pg.display.flip()
        
        pg.display.quit()
        if DEBUG: print('end')
        return

if __name__=='__main__':
    print('boo')
    DEBUG=False
    g=Gogo(SIZE)


