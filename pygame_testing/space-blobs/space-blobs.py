import sys
import pygame

from lib.options import generate_settings

## default to best display mode, assuming this is going to be the top of the list

best_mode = 0 
fullscreen = False
screen_ratio_test = False 

## settings: generate a settings object with defaults or lists of acceptable values

settings = generate_settings({
    '-fullscreen': False,
    '-mode':range(0, 30),
    '-screen_ratio_test': False,
    '-use_bluedot': False
})

print(settings)




## screen mode should be integer
try:
    best_mode = int(settings['-mode'])
except:
    best_mode 
    
##other settings to variables
fullscreen = settings['-fullscreen']
screen_ratio_test = settings['-screen_ratio_test']
use_bluedot = settings['-use_bluedot']


##test python version
python_version = sys.version_info[0]
print('python version is {0}'.format(python_version))


##test bluedot installed
from pip import get_installed_distributions

bluedot_available = len([b for b in get_installed_distributions() if 'bluedot' in b.project_name]) > 0
bd_controller = None
if bluedot_available:
    print('bluedot is available')
    if use_bluedot == True:
        print('importing bluedot')
        from bluedot import BlueDot
        bd_controller = BlueDot()
        if bd_controller:
            print('got bluedot')
            
else:
    print('bluedot is not available')


## inititalize pygame
print('initializing pygame')
pygame.init()



## get list of display modes at fullscreen to stop pixel shape going wierd
print('getting list of modes')
list_of_modes = pygame.display.list_modes(0, pygame.FULLSCREEN)

## get current display properties...
print('getting display info')
current_display = pygame.display.Info()

## .. calculate apprcx ratio
current_size = ( current_display.current_w, current_display.current_h )
current_ratio = int(100 * float(current_size[0]) / current_size[1])
print('current ratio {0}'.format(current_ratio))


 ## initialize array for close modes
good_modes = []

for m in list_of_modes:
    ratio = int(100 * float(m[0]) / m[1])
    test_ratio = abs(ratio-current_ratio) < 2
    if test_ratio or fullscreen == False or screen_ratio_test == False:
        print('{0: <4} {1: <30}'.format(len(good_modes), str(m)))
        good_modes.append(m)

print('number of good modes {0}'.format(len(good_modes)))


## start setting properties for program
size = WIDTH, HEIGHT = good_modes[best_mode]

print('current screen resolution {0}'.format(current_size))

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








NUM_STARS = 50
MAX_STAR_SPEED = -1
MIN_STAR_SPEED = -5
MAX_BLOB_SPEED = 4

'''

colours

'''

BLACK = [0, 0, 0, 0]
WHITE = (255, 255, 255, 200)


'''
font inits
'''

pygame.font.init()
myfont = pygame.font.SysFont("monospace", 15)






'''

star field

'''

import random


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
        

'''
generate stars
'''

STARS = []
for s in range(0, NUM_STARS):
    STARS.append(Star())



'''
>set GIT_SSL_NO_VERIFY=true
'''




from math import cos, sin, pi, sqrt
from random import randint


class SpaceBlob(pygame.sprite.Sprite):

    exploding = None
    EXPLODE_SIZE = 30
    
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, width, height, point=10, dir=-1):
        
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        
        self.width = width
        self.height = height
        if dir == -1:
            self.speedx = randint(-MAX_BLOB_SPEED, -2)
            self.x = randint(WIDTH, WIDTH+WIDTH)
        else:
            self.speedx = randint(2, MAX_BLOB_SPEED)
            self.x = randint(-WIDTH, 0)
                        
        
        self.speedy = 0
        self.y = randint(0, HEIGHT - self.height)       
        
        
        ## create an image for the sprite, remembering to make it transparent
        self.image = pygame.Surface([width, height])
        self.image = self.image.convert_alpha()
        self.image.fill([0, 0, 0, 0])
        self.centre = [int(width / 2), int(height / 2)]
        points = []
        for r in range(0, point):
            px = self.centre[0] + randint(int(width / 4),int(width / 2)-1) * cos(2 * pi * float(r) / point)
            py = self.centre[1] + randint(int(height / 4),int(height / 2)-1) * sin(2 * pi * float(r) / point)
            points.append([px,py])
        
        pygame.draw.polygon(self.image, WHITE, points, 2)  
        
        # define the sprites rect as that of the image
        self.rect = self.image.get_rect()
        
        ## generate mask so we can do pixel-pixel collision
        self.mask = pygame.mask.from_surface(self.image)
        
        # and because the rect inits to 0,0 top/left
        self.rect.move_ip(self.x, self.y)
        
    def move(self):
        '''
        move the space blob by the speed
        as this is a sprite we shift its rect
        '''
        self.x = self.x + self.speedx
        self.y = self.y + self.speedy
        self.rect = self.rect.move(self.speedx, self.speedy)
        
    def update(self):
        '''
        update is called directory or by the group if srite is in group.
        '''
        self.move()
        
        # if blob offscreen danger is passed
        if self.x < -self.width and self.speedx<0 or self.x + self.width > WIDTH and self.speedx>0:
            print('bye {0}'.format(self))
            self.kill()
            
        # check to see if its exploding
        if self.exploding is not None:
            self.exploding = self.exploding + 1
            self.image.fill([0, 0, 0, 0])        
            pygame.draw.circle(self.image, WHITE, self.centre, int(self.exploding+2), 3)
            if self.exploding > self.EXPLODE_SIZE:
                self.image.fill([0, 0, 0, 0])  
                self.exploding = None
                self.kill()
        
            
    def explode(self):
        if self.exploding == None: self.exploding = 0
    
            
        
        

TIME_SURVIVED = 0


space_blobs = pygame.sprite.Group()
space_group = pygame.sprite.Group()

WAVE = 0

def new_wave(num=5):
    for r in range(0,num):
        space_blobs.add(SpaceBlob(45+randint(0,10),45+randint(0,10)))


space_group = space_blobs.copy()




class SpacePerson(pygame.sprite.Sprite):

    exploding = None
    invincible = None
    EXPLODING_SIZE = 30
    INVINCIBLE_SIZE = 30
    frame = 0
    FRAMES = 8
    velocity = [2.0,0.0]
    DRAG = 0.85
    dir = (1.0, 0.0)
    thrust = 0.75

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, width=30, height=30):        
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        
        self.x = 20
        self.y = HEIGHT / 2
        self.invincible = self.INVINCIBLE_SIZE
        
        self.image_blank = pygame.Surface([width, height])
        self.image_blank = self.image_blank.convert_alpha()
        self.image_blank.fill([0, 0, 0, 0])
        
        self.image_normal = {}
        self.mask_normal = {}
        
        self.centre = [width / 2, height / 2]
        
        
        for o in range(0,self.FRAMES):
            offset = o * 2 * pi / self.FRAMES                
            image = pygame.Surface([width, height])
            image = image.convert_alpha()
            image.fill([0, 0, 0, 0])
            points = []
            
            dx = round(cos(0 + offset),2)
            dy = round(sin(0 + offset),2)
            
            
            px = self.centre[0] + (width / 2) * cos(0 + offset)
            py = self.centre[1] + (width / 2) * sin(0 + offset)            
            points.append([px,py])
            
            px = self.centre[0] + (width / 2) * cos(0.75 * pi + offset)
            py = self.centre[1] + (width / 2) * sin(0.75 * pi + offset)            
            points.append([px,py])
            
            px = self.centre[0]
            py = self.centre[1]         
            points.append([px,py])
            
            px = self.centre[0] + (width / 2) * cos(1.25 * pi + offset)
            py = self.centre[1] + (width / 2) * sin(1.25 * pi + offset)            
            points.append([px,py])
                    
            pygame.draw.polygon(image, WHITE, points, 2) 
            self.image_normal[(dx,dy)] = image
            self.mask_normal[(dx,dy)] = pygame.mask.from_surface(image)
         
        self.image = self.image_normal[(1,0)]
        self.image = self.image.convert_alpha()
        self.image.fill([0, 0, 0, 0])
        
        # define the sprites rect as that of the image
        self.rect = self.image.get_rect()
        
        ## generate mask so we can do pixel-pixel collision
        self.mask = pygame.mask.from_surface(self.image)
        
        # and because the rect inits to 0,0 top/left
        self.rect.move_ip(self.x, self.y)
        
    def move(self):
        # and because the rect inits to 0,0 top/left
         
        try:
            #print ('self.dir', self.dir)
            self.image = self.image_normal[self.dir]
            self.mask =  pygame.mask.from_surface(self.image)
        except:
            pass
            
        self.x = self.x + self.velocity[0]
        self.y = self.y + self.velocity[1]        
        
        self.rect.x = self.x
        self.rect.y = self.y
       
        self.velocity[0] = self.velocity[0] * self.DRAG
        self.velocity[1] = self.velocity[1] * self.DRAG
        
        if abs(self.velocity[0])<0.001 and abs(self.velocity[1])<0.001:
            #print('slow reset')
            self.velocity=[0,0] 
        
        
    def accell(self,dx,dy):
        
        mag = self.velocity[0]*self.velocity[0] + self.velocity[1]*self.velocity[1]
        mag = sqrt(mag)      
        
        if mag < 20.0:
            self.velocity[0] = self.velocity[0] + dx * 2
            self.velocity[1] = self.velocity[1] + dy * 2
        
        mag = self.velocity[0]*self.velocity[0] + self.velocity[1]*self.velocity[1]
        mag = sqrt(mag)
            
        if mag > 0.5:
            
            test = (round(self.velocity[0] / mag,0) , round(self.velocity[1] / mag,0))
            if abs(test[0])+abs(test[1]) == 1:
                self.dir = test
            else:
                self.dir = ( 0.71 * test[0]/abs(test[0]), 0.71 * test[1]/abs(test[1]) )            
            
        
    def update(self):    
        self.move()
        
        #print(('drag' ,  self.DRAG , 'velocity' , self.velocity))
        
        #print(self.dir)
        # define the sprites rect as that of the image
        #self.rect = self.image.get_rect()
        
        ## generate mask so we can do pixel-pixel collision
        #self.mask = pygame.mask.from_surface(self.image)
        ##print(self.velocity)
        
        
    def get_image():
        return self.image_normal[self.dir]
        
    def get_mask():
        return self.mask_normal[self.dir]
     
        

robin = SpacePerson()
space_group.add(robin)

clock = pygame.time.Clock()

## flag for running loop
running = True

keys = {}
keys[119] = False
keys[115] = False
keys[97] = False
keys[100] = False


## main game loop
while running:
    
    screen_surface.fill(BLACK)
    
    for event in pygame.event.get():
        ##print('event dict',event.type,pygame.event.event_name(event.type),event.dict)
        #if 'pos' in dir(event):
        #    print(' pos',event.pos)
        #if 'state' in dir(event):
        #    print(' state',event.state)
        #if event.type == 4:
        #    if last_mouse == None: last_mouse = event.pos
        #    pygame.draw.line(screen_surface, (255,255,255,128), last_mouse, event.pos)
        #    last_mouse = event.pos
        #    #print(event.pos)
        
            
        # quite important if you want to exit.
        # original example had just the mouse X button so added Esc for quickly exiting
        if event.type == pygame.QUIT or ( event.type == 3 and event.dict['key'] == 27):
            running = False
            back_to_normal()
        
        if 'key' in event.dict:
        
            if pygame.event.event_name(event.type) == 'KeyDown':
                #print('key down')
                keys[event.dict['key']] = True
                
            if pygame.event.event_name(event.type) == 'KeyUp':
                #print('key up')
                keys[event.dict['key']] = False

    if bd_controller is not None:
        if bd_controller.position is not None:
                if bd_controller.is_pressed == True:
                    print(bd_controller.position.x, bd_controller.position.y)
                    if bd_controller.position.x > 0.4: keys[100]=True
                    else: keys[100] = False

                    if bd_controller.position.x < -0.4: keys[97]=True
                    else: keys[97] = False

                    if bd_controller.position.y < -0.4: keys[115]=True
                    else: keys[115] = False

                    if bd_controller.position.y > 0.4: keys[119]=True
                    else: keys[119] = False

                else:
                    keys[100] = False
                    keys[97] = False
                    keys[119] = False
                    keys[115] = False

    if keys[115]: #s down
        robin.accell(0.0,robin.thrust)
    if keys[119]: #w up
        robin.accell(0.0,-robin.thrust)
    if keys[97]:  #a left
        robin.accell(-robin.thrust,0.0)
    if keys[100]: #d right
        robin.accell(robin.thrust,0.0)
        
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
        WAVE = WAVE + 1
        new_wave(WAVE)
        
    
    robin.update()
    space_blobs.draw(screen_surface)
    space_group.draw(screen_surface)
    
    
    ## collision of blob with spaceperson
    main_list = pygame.sprite.groupcollide(space_blobs, space_group, False, False, collided=None)
    for blob in main_list:
        for person in main_list[blob]:
            if pygame.sprite.collide_mask(person, blob) is not None:
                if blob.exploding == None: blob.explode()
            
    
    # make a sticker, like a dymo...
    label = myfont.render('{0:03d} {1:05d} {2:02d}'.format(WAVE, TIME_SURVIVED, len(space_blobs.sprites())  ), 1, WHITE)
    
    # ...stick it to the telly
    screen_surface.blit(label, (WIDTH/2 - label.get_width()/2, HEIGHT - 20))  

    # 40 fps should be enough for anyone
    clock.tick(40)
    
    # update the buffer (draw!)
    pygame.display.update()
    TIME_SURVIVED = TIME_SURVIVED + 1



print('done')
pygame.quit()
