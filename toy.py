import pygame
from random import random, randint
from collections import namedtuple
from numpy import int32

# ~DEFINES
X = 0
Y = 1
Unit = namedtuple('Unit', 'position sprite state')

# Globals, UGLY!
done = False
man_sprite = None

def load_assets():
    global man_sprite
    man_sprite = pygame.image.load('assets/dude.png').convert_alpha()
    pixels = pygame.surfarray.pixels2d( man_sprite )
    
def recolor_sprite(sprite):
    pixels = pygame.surfarray.pixels2d( sprite )
    #print hex(pixels[0][0] & (2**32-1))
    #print hex(pixels[15][25] & (2**32-1))
    #print hex(pixels[25][15] & (2**32-1))
    
    a = 255
    r = randint(70,200)
    g = randint(70,200)
    b = randint(70,200)
    light_shirt_color = a*256**3+r*256**2 + g*256 + b
    dark_shirt_color = a*256**3+(r-50)*256**2 + (g-50)*256 + (b-50)
    
    for x in xrange(len(pixels)):
        for y in xrange(len(pixels[0])):
	    if pixels[x][y]==int32(0xFF8E524A):
                pixels[x][y] = int32(light_shirt_color)
	    if pixels[x][y]==int32(0xFF603833):
		pixels[x][y] = int32(dark_shirt_color)

def update(units):
    for unit in units:       
	unit.position[X] = unit.position[X]+randint(-1,1) 
	unit.position[Y] = unit.position[Y]+randint(-1,1)
        
def draw(screen, units):
    global man_sprite
    
    screen.fill((255, 255, 255)) 
    
    for unit in units:
	screen.blit(unit.sprite, unit.position)
    
    pygame.display.update()
    
    
def handle_input_events():
    for event in pygame.event.get():
	if event.type == pygame.QUIT:
	    on_esc_pressed()

def on_esc_pressed():
    global done
    done = True
    
## Pygame initialization ##
pygame.init()
size = [640, 480]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Culture Ritual')
clock = pygame.time.Clock()

load_assets()

## Variable initialization ##
units = []
for i in xrange(100):
    unit_man_sprite = man_sprite.copy()
    recolor_sprite(unit_man_sprite)
    
    new_unit = Unit(
	position=[randint(0,size[X])-30, randint(0,size[Y])-50],
	sprite=unit_man_sprite,
	state = None) #state undefined for now
    units.append( new_unit )

    
## Main game loop ##
nloop = 0
while done == False:
    
    # inputs
    handle_input_events()
    
    # update state
    update(units)
    
    # screen draw
    draw(screen, units)
     
    # run at X fps
    clock.tick(5)
    
    pygame.image.save(screen, "screenshot%02d.tga" % nloop)
    nloop+=1
 
# close the window and quit
pygame.quit()
