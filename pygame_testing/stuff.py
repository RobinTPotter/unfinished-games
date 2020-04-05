#! /usr/bin/python3
import sys
import pygame as pg
import threading
import argparse
from math import sin, cos, pi

SIZE = (640,480)
DEBUG=True

'''

import stuff
g = stuff.Gogo()
l = stuff.Level()
l.length = 40
l.rot = [0,0,0]+[-10 for a in range(0,180,10)]+[0,0,0,0]
l.gen()
g.lines = [l.outer_lines, l.inner_lines, l.wall_lines]

def poo(point):
    return point[0]-1+randint(0,1), point[1]-1+randint(0,1)

g.tf = poo

'''

# args = argparse.init()

def depth(tup,dep=10):
    return (
        (tup[0])/dep,
        (tup[1])/dep
    )

class Level():
    def __init__(self, size=SIZE):
        self.closed = False
        self.size=size
        self.init_start = (-220,-220)
        self.length = 38
        self.init_rot = 90
        self.rot = [10,10,10,-10,-10,-10]
        self.depth = 10

    def gen(self):
        self.closed = False
        size = self.size
        start = self.init_start
        self.outer_lines = []
        self.inner_lines = []
        self.wall_lines = []
        current_a = self.init_rot
        saved_start_top = None
        saved_start_bottom = None
        for a in self.rot:
            current_a = current_a + a

            end = (start[0]+self.length*cos(2* pi * current_a/360), \
                start[1]+self.length*sin(2* pi * current_a/360) )

            if saved_start_top is None: saved_start_top = (start[0]+size[0]/2,start[1]+size[1]/2)

        
            self.outer_lines.append((start[0]+size[0]/2,start[1]+size[1]/2))
            self.outer_lines.append((end[0]+size[0]/2,end[1]+size[1]/2))

            deep_start = depth(start,dep=self.depth)
            deep_end = depth(end,dep=self.depth)

            self.inner_lines.append((deep_start[0]+size[0]/2,deep_start[1]+size[1]/2))
            self.inner_lines.append((deep_end[0]+size[0]/2,deep_end[1]+size[1]/2))

            if saved_start_bottom is None: saved_start_bottom = (deep_start[0]+size[0]/2,deep_start[1]+size[1]/2)


            self.wall_lines.append((end[0]+size[0]/2,end[1]+size[1]/2))
            self.wall_lines.append((deep_end[0]+size[0]/2,deep_end[1]+size[1]/2))

            start = end
        if start == self.init_start:
            self.closed = True
        else:
            self.wall_lines.append(saved_start_top)
            self.wall_lines.append(saved_start_bottom)




class Colours():
    blue = (0,0,255)
    red = (255,0,0)
    darkRed = (128,0,0)
    green = (0,255,0)
    darkGreen = (0,128,0)
    darkBlue = (0,0,128)
    white = (255,255,255)
    darkGrey = (64,64,64)
    grey = (128,128,128)
    black = (0,0,0)
    pink = (255,200,200)

class Gogo():
    def __init__(self,size=(640,480)):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(size)
        #self.lines = [[ (10,10), (20,20)]]
        self.level = Level()
        self.level.gen()
        self.lines = [self.level.outer_lines,self.level.inner_lines,self.level.wall_lines]
        self.working = True
        self.thread = threading.Thread(target=self.gogo)
        if DEBUG: print('starting thread')
        self.thread.start()
   
    def get_working(self):
        return self.working

    def tf(self,point):
        return point

    def gogo(self):
        print('gogo')
        while self.get_working():
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.working = False

            self.screen.fill(Colours.darkBlue)
            for ls in self.lines:
                for ll in range(0,len(ls),2):
                    pg.draw.line(self.screen, Colours.white, self.tf(ls[ll]), self.tf(ls[ll+1]), 1)

            pg.display.update()
            self.clock.tick(25)
        
        pg.display.quit()
        if DEBUG: print('end')
        return

if __name__=='__main__':
    print('boo')
    DEBUG=False
    g=Gogo(SIZE)
