
import sys
import pygame


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
    if test_ratio:
        print (m)
        good_modes.append(m)

print 'number of good modes {0}'.format(len(good_modes))


## default to best display mode, assuming this is going to be the top of the list

best_mode = 0 

## user starts with integer
print sys.argv
if len(sys.argv)>1: best_mode = int(sys.argv[1])

## start setting properties for program
size = width, height = good_modes[best_mode]

print current_size

## inititalize a drawing surface
screen_surface = pygame.display.set_mode(size, pygame.FULLSCREEN)

## switch off the mouse pointer
pygame.mouse.set_visible(False)

## inititalize a variable to hold the mouse position, could be an array for 'tail' eg.
last_mouse = None

## flag for running loop
running = True


## declare function for returning to orignanl state (assuming full screen at the mo)
def back_to_normal():
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
