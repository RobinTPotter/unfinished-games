#! /usr/bin/python3
import sys
import pygame as pg
import threading
import argparse
from math import sin, cos, pi

SIZE = (640, 480)
DEBUG=True


'''

import stuff
g = stuff.Gogo()
l = stuff.Level()
l.length = 40
l.rot = [0,0,0]+[-10 for a in range(0,180,10)]+[0,0,0,0]
l.gen()
g.lines = [l.outer_lines, l.inner_lines, l.wall_lines]


from random import randint

def poo(point):
    return point[0]-1+randint(0,1), point[1]-1+randint(0,1)

g.tf = poo

'''

# args = argparse.init()

class Point():
    def __init__(self, x=0, y=0, *args):
        self.x=x
        self.y=y
        if isinstance(args, (tuple)) and len(args)==2:
            self.x = args[0]
            self.y = args[1]
    
    def __add__(self, point):
        if isinstance(point,Point):
            return Point(self.x+point.x,self.y+point.y)
        elif isinstance(point,(int,float)):
            return Point(self.x+point,self.y+point)
        else:
            print('operation not allowed add {} to {}'.format(self, point))
            return None

    def __mul__(self, point):
        if isinstance(point,Point):
            return Point(self.x*point.x,self.y*point.y)
        elif isinstance(point,(int,float)):
            return Point(self.x*point,self.y*point)
        else:
            print('operation not allowed mult {} to {}'.format(self, point))
            return None
            
    def __truediv__(self, point):
        if isinstance(point,Point):
            return Point(self.x/point.x,self.y/point.y)
        elif isinstance(point,(int,float)):
            return Point(self.x/point,self.y/point)
        else:
            print('operation not allowed truediv {} to {}'.format(self, point))
            return None
    
    def tup(self):
        return (self.x, self.y)
        




class Level():
    def __init__(self, size=SIZE):
        self.closed = False
        self.size = size
        self.init_start = Point(-220,-120)
        self.length = 38
        self.init_rot = 90
        self.rot = [0,0,0] + [-10 for a in range(12)] +[10,10,10]
        self.depth = 10

    def gen(self):
        self.closed = False
        size = self.size
        middle = Point (self.size[0] / 2, self.size[1] / 2)
        start = self.init_start
        self.outer_lines = []
        self.inner_lines = []
        self.wall_lines = []
        current_a = self.init_rot
        saved_start_top = None
        saved_start_bottom = None
        centre = Point(SIZE[0],SIZE[1])
        for a in self.rot:
            current_a = current_a + a
            next =  Point(self.length * cos(2 * pi * current_a / 360),self.length * sin(2 * pi * current_a / 360))
            end = start + next
            if saved_start_top is None: saved_start_top =start + middle
            self.outer_lines.append(start + middle)
            self.outer_lines.append(end + middle)
            deep_start = start / self.depth
            deep_end = end / self.depth
            self.inner_lines.append(deep_start + middle)
            self.inner_lines.append(deep_end + middle)
            if saved_start_bottom is None: saved_start_bottom = (deep_start + middle)
            self.wall_lines.append(end + middle)
            self.wall_lines.append(deep_end + middle)
            start = end
        if start == self.init_start:
            self.closed = True
        else:
            self.wall_lines.append(saved_start_top)
            self.wall_lines.append(saved_start_bottom)

class Colours():
    blue = (0, 0, 255)
    red = (255, 0, 0)
    darkRed = (128, 0, 0)
    green = (0, 255, 0)
    darkGreen = (0, 128, 0)
    darkBlue = (0, 0, 128)
    white = (255, 255, 255)
    darkGrey = (64, 64, 64)
    grey = (128, 128, 128)
    black = (0, 0, 0)
    pink = (255, 200, 200)

class Gogo():
    def __init__(self, size=(640, 480)):
        self.clock = pg.time.Clock()
        #self.lines = [[ (10,10), (20,20)]]
        self.level = Level()
        self.level.gen()
        #self.lines = [self.level.outer_lines, self.level.inner_lines, self.level.wall_lines]
        self.working = True
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
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.working = False

            self.screen.fill(Colours.darkBlue)
            lines = self.level.outer_lines+self.level.wall_lines+self.level.inner_lines
            for ll in range(0, len(lines), 2):
                pg.draw.line(self.screen, Colours.white, self.tf(lines[ll]).tup(), self.tf(lines[ll+1]).tup(), 1)

            self.clock.tick(40)
            pg.display.flip()
        
        pg.display.quit()
        if DEBUG: print('end')
        return

if __name__=='__main__':
    print('boo')
    DEBUG=False
    g=Gogo(SIZE)
