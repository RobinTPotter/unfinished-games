
import sys
import pygame

pygame.init()

size = width, height = 800, 600

current_display = pygame.display.Info()

current_size = [ current_display.current_w, current_display.current_h ]

print current_size

screen_surface = pygame.display.set_mode(size, pygame.FULLSCREEN)

pygame.mouse.set_visible(False)

running = True

def back_to_normal():
    pygame.display.set_mode(current_size)
    pygame.quit()
    running = False
    print 'quit'

while running:
    for event in pygame.event.get():
        #print event.type
        #for x in dir(pygame):
        #    if str(type(getattr(pygame,x)))=='<type \'int\'>':
        #        print(x,getattr(pygame,x))
        #print('event dict',event.type,pygame.event.event_name(event.type),event.dict)
        #if 'pos' in dir(event):
        #    print (' pos',event.pos)
        #if 'state' in dir(event):
        #    print (' state',event.state)
        if event.type == 4:
            pygame.draw.line(screen_surface, (255,255,255,128), event.pos, event.pos)
            print event.pos
        if event.type == pygame.QUIT or ( event.type == 3 and event.dict['key'] == 27):
            back_to_normal()
            
        pygame.display.update()

print 'done'


