import pygame
import sys
import time 

pygame.init()

size = width, height = 640, 480


screen = pygame.display.set_mode(size)

ball = pygame.image.load("64_64_alpha.png").convert_alpha()
bg = pygame.image.load("640_480_back.png").convert()

ballrect = ball.get_rect()

clock = pygame.time.Clock()

print (ballrect, dir(ballrect))

black = [1,0,0]
speed = [1,1]

screen.fill(black)
screen.blit(bg, bg.get_rect())
pygame.display.update()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.blit(bg, bg.get_rect())
    screen.blit(ball, ballrect)
    pygame.display.update(pygame.Rect(ballrect.left - 10, ballrect.top - 10, 84, 84))
    clock.tick(40)

