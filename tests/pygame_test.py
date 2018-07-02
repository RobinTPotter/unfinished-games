
import pygame as pg
import os
import json
import time
import random

pg.init()
pg.joystick.init()
joystick = None


pg.font.init()
font = pg.font.SysFont(None, 12)
print (font)

config_file = 'config.file.txt'

def save_config(config):
    with open(config_file,'w') as fp:
        fp.write(json.dumps(config))

def load_config():
    if config_file in os.listdir('.'):
        with open(config_file,'r') as fp:
            print ("reading config: {0}".format(config_file))
            return json.loads(fp.read())
    else:
        print("no config found: {0}".format(config_file))
        return {'size': [200,150], \
                'FPS': 40 \
                }

config = load_config()
save_config(config)




pg.display.set_mode(config['size'])
FPS = config['FPS']


class main_screen :
    screen = None
    textsurface_counter = 0 
    
    def __init__(self):
        "Ininitializes a new pg screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print("I'm running under X display = {0}".format(disp_no))
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pg.display.init()
            except pg.error:
                print('Driver: {0} failed.'.format(driver))
                continue
            found = True
            print('Driver: {0} assigned.'.format(driver))
            break
    
        if not found:
            raise Exception('No suitable video driver found!')
        
        size = (pg.display.Info().current_w, pg.display.Info().current_h)
        print("Framebuffer size: {0} x {1}".format(size[0], size[1]))
        self.screen = pg.display.set_mode(size, pg.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))        
        # Initialise font support
        pg.font.init()
        # Render the screen
        pg.display.update()
 
    def joystick_setup(self):                
        try:
            for j in range(pg.joystick.get_count()):
                self.output("attemp connect to joysticks {0}".format(j))
                joystick = pg.joystick.Joystick(j)
                name = joystick.get_name()
                if 'last_joystick' not in config is None or config['last_joystick']==name:
                    joystick.init()
                    if 'last_joystick' not in config:
                        config['last_joystick'] = name
                        save_config(config)
                    
                    self.output("{0} initialized".format(name))
        except:
            self.output("no joysticks")
            
    def output(self, message):
        print(message)
        self.textsurface = font.render(message, True, (0, 0, 0),(255,255,255))
        self.textsurface_counter = 255
            
    def __del__(self):
        "Destructor to make sure pg shuts down, etc."
 
    def test(self,clock):

        done = False
        try:    
            while done==False:
                
                # Fill the screen with red (255, 0, 0)
                red = (255, 0, 0)
                self.screen.fill(red)
                # Update the display
                
                if self.textsurface_counter > 0:
                    self.screen.blit(self.textsurface,(0,0))
                    self.textsurface.set_alpha(self.textsurface_counter)
                    self.textsurface_counter -= 10
                    #print("zzzz {0}".format(self.textsurface_counter))
                    
                # EVENT PROCESSING STEP
                for event in pg.event.get(): # User did something
                    if event.type == pg.QUIT or ( event.type == pg.KEYDOWN and event.key == 27 ): # If user clicked close
                        done=True # Flag that we are done so we exit this loop
                    
                    # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
                    if event.type == pg.JOYBUTTONDOWN or ( event.type == pg.KEYDOWN ):
                        self.output("Joystick button pressed or key "+str(event.key)+" pressed")
                        
                    if event.type == pg.JOYBUTTONUP or ( event.type == pg.KEYUP ):
                        self.output("Joystick button released or key "+str(event.key)+" released")
                        
                clock.tick(FPS)
                pg.display.flip()
                
        except Exception as al:
            print("{0}".format(al))
            pass

        pg.quit()




if __name__ == "__main__":
    # Create an instance of the class
    clock = pg.time.Clock()
    player = main_screen()
    player.test(clock)