
import sys
import pygame
import json
import os


## default to best display mode, assuming this is going to be the top of the list

best_mode = 0 
fullscreen = False
no_screen_ratio_test = False 

## settings

settings = {}

options = {
    '-fullscreen': False,
    '-mode':range(0,30),
    '-no_screen_ratio_test': False
}

if len(sys.argv) > 1:
    settings = options
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
                    print 'value {0} is invalid for setting {1}'.format(value,key)
                    
    with open('settings.json','w') as sf:
        sf.write(json.dumps(settings))
        
            
else:
    files = os.listdir('.')
    if 'settings.json' in files:
        with open('settings.json','r') as sf:
            settings = json.loads(sf.read())


print settings


## user starts with integer
best_mode = int(settings['-mode'])
fullscreen = settings['-fullscreen']


## inititalize pygame
pygame.init()



## get list of display modes at fullscreen to stop pixel shape going wierd
list_of_modes = pygame.display.list_modes(0, pygame.FULLSCREEN)

## get current display properties...
current_display = pygame.display.Info()

## .. calculate apprcx ratio
current_size = ( current_display.current_w, current_display.current_h )
current_ratio = int(100*float(current_size[0])/current_size[1])
print current_ratio


 ## initialize array for close modes
good_modes = []

for m in list_of_modes:
    ratio = int(100*float(m[0])/m[1])
    test_ratio = abs(ratio-current_ratio) < 2
    if test_ratio or fullscreen == False or no_screen_ratio_test:
        print '{0: <4}   {1: <30}'.format(len(good_modes), m)
        good_modes.append(m)

print 'number of good modes {0}'.format(len(good_modes))


## start setting properties for program
size = width, height = good_modes[best_mode]

print 'current screen resolution {0}'.format(current_size)

## inititalize a drawing surface
if fullscreen == True:
    screen_surface = pygame.display.set_mode(size, pygame.FULLSCREEN)
else:
    screen_surface = pygame.display.set_mode(size)

## switch off the mouse pointer
pygame.mouse.set_visible(False)

## inititalize a variable to hold the mouse position, could be an array for 'tail' eg.
last_mouse = None

## flag for running loop
running = True


## declare function for returning to orignanl state (assuming full screen at the mo)
def back_to_normal():
    if fullscreen:
        pygame.display.set_mode(current_size)
    pygame.quit()
    running = False
    print 'quit'

## main game loop
while running:
    for event in pygame.event.get():
        #print('event dict',event.type,pygame.event.event_name(event.type),event.dict)
        #if 'pos' in dir(event):
        #    print (' pos',event.pos)
        #if 'state' in dir(event):
        #    print (' state',event.state)
        if event.type == 4:
            if last_mouse == None: last_mouse = event.pos
            pygame.draw.line(screen_surface, (255,255,255,128), last_mouse, event.pos)
            last_mouse = event.pos
            #print event.pos
        
        # quite important if you want to exit.
        # original example had just the mouse X button so added Esc for quickly exiting
        if event.type == pygame.QUIT or ( event.type == 3 and event.dict['key'] == 27):
            back_to_normal()
            
        # update the buffer (draw!)
        pygame.display.update()

print 'done'
