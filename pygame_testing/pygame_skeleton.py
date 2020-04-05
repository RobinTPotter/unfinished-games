#! /usr/bin/python3
import sys
import pygame as pg

pg.init()

class Colours():
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    darkBlue = (0,0,128)
    white = (255,255,255)
    black = (0,0,0)
    pink = (255,200,200)

screen = pg.display.set_mode((640,480))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    screen.fill(Colours.darkBlue)
    pg.draw.lines(screen, Colours.white, False, [(10,10),(20,20)], 1)
    pg.display.update()

