import pygame
from random import random, randint
from collections import namedtuple

# ~DEFINES
X = 0
Y = 1
Unit = namedtuple('Unit', 'position state')


man_sprite = None
def load_assets():
    global man_sprite
    man_sprite = pygame.image.load('assets/dude.png')

def update(units):
    for unit in units:       
	unit.position[X] = unit.position[X]+randint(-1,1) 
	unit.position[Y] = unit.position[Y]+randint(-1,1)
        
def draw(screen, units):
    global man_sprite
    
    screen.fill((255, 255, 255)) 
    
    for unit in units:
	print man_sprite, unit.position
	screen.blit(man_sprite, unit.position)
    
    pygame.display.update()
    
    
def handle_input_events():
    for event in pygame.event.get():
	if event.type == pygame.QUIT:
	    on_esc_pressed()

def on_esc_pressed():
    done = True
    
## Pygame initialization ##
pygame.init()
size = [640, 480]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Culture Ritual')
clock = pygame.time.Clock()

## Variable initialization ##
units = []
for i in xrange(100):
    new_unit = Unit(
    position=[randint(0,size[X])-30, randint(0,size[Y])-50],
    state = None) #state undefined for now
    units.append( new_unit )
load_assets()
    
## Main game loop ##
done = False
nloop = 0
while done == False:
    
    # inputs
    handle_input_events()
    
    # update state
    update(units)
    
    # screen draw
    draw(screen, units)
     
    # run at 20 fps
    clock.tick(10)
    
    pygame.image.save(screen, "screenshot%02d.tga" % nloop)
    nloop+=1
 
# close the window and quit
pygame.quit()
