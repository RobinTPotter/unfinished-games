"""
bluedot controlled swearbox.

use config to list words, as many as you like
depending on how small your fingers are.

pair your device to your computer
connect, and start bluedot

"""



from bluedot import BlueDot
from math import pi, atan
from subprocess import Popen
from config import swearwords, delay
import time

# initialize blue dot
bd = BlueDot()

# dict to hold properties for words we want to shout
swearbox = {}

NUMWORDS = len(swearwords)

# make a dictionary of words
# the index is a number
# because we will refer to the word by
# its position on the blue dot
# has a couple of properties:
#  on: is last used
#  word: the actual word
for num in range(NUMWORDS):
    swearbox[num] = {}
    swearbox[num]['on'] = 0
    swearbox[num]['word'] = swearwords[num]
    swearbox[num]['delay'] = delay

print(swearbox)


# vector class to hide finding the angle of a vector
class vector():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return str(self.x)+','+str(self.y)
    
    def angle(self):
        if (self.y==0):
            if (self.x>0):
                return 0
            else:
                return pi
                
        elif (self.x==0):
            if (self.y>0):
                return pi/2
            else:
                return 3*pi/2
        else:
            ang = abs(atan(self.y/self.x))            
            if (self.x>0 and self.y>0):
                return ang
            elif (self.x>0 and self.y<0):
                return 2*pi - ang
            elif (self.x<0 and self.y>0):
                return pi - ang
            elif (self.x<0 and self.y<0):
                return pi + ang


# use espeak to speak the word
def curse(word):
    Popen(['espeak', word])


def dot_pressed(position):        
    # find the position of finger, find angle
    v = vector(position.x, position.y)
    angle = v.angle()    
    # word number is based on the arc, if that's the right word
    word = int(NUMWORDS * angle / (2 * pi))# check if word used less than X ago
    if (time.time() - swearbox[word]['on']) > swearbox[word]['delay']:                
        #no so..
        swearbox[word]['on'] = time.time()
        #use your words
        curse(swearbox[word]['word'])
   
# went mad before dicovering these assignments
bd.when_pressed = dot_pressed
bd.when_moved = dot_pressed

while True:
    pass
