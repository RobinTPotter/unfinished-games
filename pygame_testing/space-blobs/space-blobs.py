import sys
import pygame
import json
import os


## default to best display mode, assuming this is going to be the top of the list

best_mode = 0 
fullscreen = False
screen_ratio_test = False 

## settings

settings = {}

options = {
    '-fullscreen': False,
    '-mode':range(0, 30),
    '-screen_ratio_test': False
}

settings = options

if len(sys.argv) > 1:
    for key in options.keys():
        if key in sys.argv:
            print '{0} found'.format(key)
            pos = sys.argv.index(key)
            print 'key positions {0}'.format(pos)
            value = None
            if type(options[key]) is not bool:
                print 'key not bool {0} {1} {2}'.format(key, options[key], type(options[key]))
                value = sys.argv[pos + 1]
            if value == None:
                settings[key] = True
            else:
                if str(value) in [str(o) for o in options[key]]:
                    settings[key] = str(value)
                else:
                    print 'value {0} is invalid for setting {1}'.format(value, key)
                    
    with open('settings.json', 'w') as sf:
        sf.write(json.dumps(settings))
        
            
else:
    files = os.listdir('.')
    if 'settings.json' in files:
        with open('settings.json', 'r') as sf:
            settings = json.loads(sf.read())


print settings


## user starts with integer
try:
    best_mode = int(settings['-mode'])
except:
    best_mode 
fullscreen = settings['-fullscreen']
screen_ratio_test = settings['-screen_ratio_test']

## inititalize pygame
pygame.init()



## get list of display modes at fullscreen to stop pixel shape going wierd
list_of_modes = pygame.display.list_modes(0, pygame.FULLSCREEN)

## get current display properties...
current_display = pygame.display.Info()

## .. calculate apprcx ratio
current_size = ( current_display.current_w, current_display.current_h )
current_ratio = int(100 * float(current_size[0]) / current_size[1])
print current_ratio


 ## initialize array for close modes
good_modes = []

for m in list_of_modes:
    ratio = int(100 * float(m[0]) / m[1])
    test_ratio = abs(ratio-current_ratio) < 2
    if test_ratio or fullscreen == False or screen_ratio_test == False:
        print '{0: <4} {1: <30}'.format(len(good_modes), m)
        good_modes.append(m)

print 'number of good modes {0}'.format(len(good_modes))


## start setting properties for program
size = WIDTH, HEIGHT = good_modes[best_mode]

print 'current screen resolution {0}'.format(current_size)

## inititalize a drawing surface
if fullscreen == True:
    screen_surface = pygame.display.set_mode(size, pygame.FULLSCREEN)
else:
    screen_surface = pygame.display.set_mode(size)

## switch off the mouse pointer
pygame.mouse.set_visible(False)

##change name to space blobs
pygame.display.set_caption('space blobs')

## inititalize a variable to hold the mouse position, could be an array for 'tail' eg.
last_mouse = None

## flag for running loop
running = True


## declare function for returning to orignanl state (assuming full screen at the mo)
def back_to_normal():
    if fullscreen:
        pygame.display.set_mode(current_size)
    pygame.quit()
    sys.exit(0)









'''

star field

'''

import random

NUM_STARS = 10
MAX_STAR_SPEED = -1
MIN_STAR_SPEED = -5

class Star():
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.s = random.randint(MIN_STAR_SPEED, MAX_STAR_SPEED)

    def zoom(self):
        self.x = self.x + self.s
        if self.x > WIDTH:
            self.x = 0 
            self.y = random.randint(0, HEIGHT)
            self.s = random.randint(MIN_STAR_SPEED, MAX_STAR_SPEED)
        elif self.x < 0:
            self.x = WIDTH 
            self.y = random.randint(0, HEIGHT)
            self.s = random.randint(MIN_STAR_SPEED, MAX_STAR_SPEED)
        

STARS = []
for s in range(0, NUM_STARS):
    STARS.append(Star())


'''

colours

'''

BLACK = [0, 0, 0]
WHITE = (255, 255, 255, 30)




'''
>set GIT_SSL_NO_VERIFY=true
'''



from math import cos, sin, pi
from random import randint


class SpaceBlob(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, width, height, point=10):
        self.x = randint(0, WIDTH)
        self.y = randint(0, HEIGHT)
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill([0, 0, 0, 0])
        centre = [width / 2, height / 2]
        points = []
        for r in range(0, point):
            px = centre[0] + randint(width / 4,width / 2) * cos(2 * pi * float(r) / point)
            py = centre[1] + randint(height / 4,height / 2) * sin(2 * pi * float(r) / point)
            points.append([px,py])
        
        pygame.draw.polygon(self.image, WHITE, points)  
        self.rect = self.image.get_rect()
        self.move(self.x, self.y)
        
    def move(self,dx,dy):
        self.x = self.x + dx
        self.y = self.y + dy
        self.rect = self.rect.move(dx, dy)



test = SpaceBlob(60,40)
test1 = SpaceBlob(60,50)




space_blobs = pygame.sprite.Group()

space_blobs.add(test)
space_blobs.add(test1)



clock = pygame.time.Clock()


## main game loop
while running:
    
    screen_surface.fill(BLACK)
    
    for event in pygame.event.get():
        #print('event dict',event.type,pygame.event.event_name(event.type),event.dict)
        #if 'pos' in dir(event):
        #    print (' pos',event.pos)
        #if 'state' in dir(event):
        #    print (' state',event.state)
        #if event.type == 4:
        #    if last_mouse == None: last_mouse = event.pos
        #    pygame.draw.line(screen_surface, (255,255,255,128), last_mouse, event.pos)
        #    last_mouse = event.pos
        #    #print event.pos
        
            
        # quite important if you want to exit.
        # original example had just the mouse X button so added Esc for quickly exiting
        if event.type == pygame.QUIT or ( event.type == 3 and event.dict['key'] == 27):
            back_to_normal()
            
            
            
    for s in STARS:
        pygame.draw.line(screen_surface, WHITE, [s.x, s.y], [s.x + s.s, s.y])
        s.zoom()
            
    for s in space_blobs.sprites():
        print s
        s.move(-1, 0)
        
    space_blobs.draw(screen_surface)
            
    clock.tick(40)
    # update the buffer (draw!)
    pygame.display.update()



