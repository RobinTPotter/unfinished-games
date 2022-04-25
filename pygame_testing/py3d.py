import pygame as pg

pg.init()

pg.display.init()
size = [640,480]
screen = pg.display.set_mode(size)
clock = pg.time.Clock()

p = [
    [-20.0,20.0,20.0],[20.0,20.0,20.0],[20.0,-20.0,20.0],[-20.0,-20.0,20.0],
    [-20.0,20.0,-20.0],[20.0,20.0,-20.0],[20.0,-20.0,-20.0],[-20.0,-20.0,-20.0]
]


l = [
	[0,1],[1,2],[2,3],[3,0],
	[4,5],[5,6],[6,7],[7,4],
	[0,4],[1,5],[2,6],[3,7]
]

n = 10
while True:

	screen.fill([0,0,0])
	for ll in l:
		pg.draw.line(
			screen,
			(250,250,50),
			(size[0]/2 + n * p[ll[0]][0]/p[ll[0]][2],size[1]/2 - n * p[ll[0]][1]/p[ll[0]][2]),
			(size[0]/2 + n * p[ll[1]][0]/p[ll[1]][2],size[1]/2 - n * p[ll[1]][1]/p[ll[1]][2]),
			1)

	pg.draw.line(screen,(250,250,250),(0,0),(100,100),2)
	clock.tick_busy_loop(15)
	pg.display.flip()
