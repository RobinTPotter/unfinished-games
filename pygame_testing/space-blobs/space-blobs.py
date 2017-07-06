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



## declare function for returning to orignanl state (assuming full screen at the mo)
def back_to_normal():
    if fullscreen:
        pygame.display.set_mode(current_size)









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

BLACK = [0, 0, 0, 0]
WHITE = (255, 255, 255, 200)




'''
>set GIT_SSL_NO_VERIFY=true
'''


MAX_BLOB_SPEED = 4


from math import cos, sin, pi
from random import randint


class SpaceBlob(pygame.sprite.Sprite):

    exploding = None

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, width, height, point=10, dir=-1):
        
        self.width = width
        self.height = height
        if dir == -1:
            self.speedx = randint(-MAX_BLOB_SPEED, -2)
            self.x = randint(WIDTH, WIDTH+WIDTH)
        else:
            self.speedx = randint(2, MAX_BLOB_SPEED)
            self.x = randint(-WIDTH, 0)
            
            
        print self.speedx
        
        self.speedy = 0
        self.y = randint(0, HEIGHT - self.height)
        
        
        print (self.x, self.y)
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image = self.image.convert_alpha()
        self.image.fill([0, 0, 0, 0])
        self.centre = [width / 2, height / 2]
        points = []
        for r in range(0, point):
            px = self.centre[0] + randint(width / 4,width / 2-1) * cos(2 * pi * float(r) / point)
            py = self.centre[1] + randint(height / 4,height / 2-1) * sin(2 * pi * float(r) / point)
            points.append([px,py])
        
        pygame.draw.polygon(self.image, WHITE, points, 2)  
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        # and because the rect inits to 0,0
        self.rect.move_ip(self.x, self.y)
        
    def move(self):
        self.x = self.x + self.speedx
        self.y = self.y + self.speedy
        self.rect = self.rect.move(self.speedx, self.speedy)
        
    def update(self):
        self.move()
        if self.x < -self.width and self.speedx<0 or self.x + self.width > WIDTH and self.speedx>0:
            print 'bye {0}'.format(self)
            self.kill()
        if self.exploding is not None:
            self.exploding = self.exploding + 1
            self.image.fill([0, 0, 0, 0])        
            pygame.draw.circle(self.image, WHITE, self.centre, int(self.exploding+2), 3)
            if self.exploding > 30:
                self.image.fill([0, 0, 0, 0])  
                self.exploding = None
                self.kill()
        
            
    def explode(self):
        if self.exploding == None: self.exploding = 0
    
            
        
        


pygame.font.init()
myfont = pygame.font.SysFont("monospace", 15)

time_so_far = 0


space_blobs = pygame.sprite.Group()

wave = 0

def new_wave(num=5):
    for r in range(0,num):
        space_blobs.add(SpaceBlob(45+randint(0,10),45+randint(0,10)))
        



clock = pygame.time.Clock()

## flag for running loop
running = True

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
            running = False
            back_to_normal()
            
            
            
    for s in STARS:
        pygame.draw.line(screen_surface, WHITE, [s.x, s.y], [s.x + s.s, s.y])
        s.zoom()
            
    
    for s1 in space_blobs.sprites():
        for s2 in space_blobs.sprites():
            if s1 is not s2 and pygame.sprite.collide_mask(s1, s2) is not None:
                if s1.exploding == None: s1.explode()
                if s2.exploding == None: s2.explode()
            
    
    space_blobs.update()
        
    if len(space_blobs.sprites()) == 0:
        wave = wave + 1
        new_wave(wave)
        
    space_blobs.draw(screen_surface)
    
    
    #screen_surface = font.render('{0: <3} {1: <3}'.format(wave, time_so_far),True, WHITE, )
    label = myfont.render('{0:03d} {1:05d} {2:02d}'.format(wave, time_so_far, len(space_blobs.sprites())), 1, WHITE)
    screen_surface.blit(label, (WIDTH/2 - label.get_width()/2, HEIGHT - 20))  

      
    clock.tick(40)
    # update the buffer (draw!)
    pygame.display.update()
    time_so_far = time_so_far + 1



print 'done'
pygame.quit()