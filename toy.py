import pygame
from random import random, randint
from collections import namedtuple
from numpy import int32, int64
import platform
if platform.architecture()[0]=='32bit':
    color_bit_conversion = int64
else:
    color_bit_conversion = int32

#import os, sys
#sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import pop

# ~DEFINES
X = 0
Y = 1


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
    #print(pixels[15][25], hex(pixels[15][25]))
    
    a = 255
    r = randint(70,200)
    g = randint(70,200)
    b = randint(70,200)
    light_shirt_color = a*256**3+r*256**2 + g*256 + b
    dark_shirt_color = a*256**3+(r-50)*256**2 + (g-50)*256 + (b-50)
    
    for x in range(len(pixels)):
        for y in range(len(pixels[0])):
            if pixels[x][y]==color_bit_conversion(0xFF8E524A):
                pixels[x][y] = color_bit_conversion(light_shirt_color)
            if pixels[x][y]==color_bit_conversion(0xFF603833):
                pixels[x][y] = color_bit_conversion(dark_shirt_color)

def update(units):
    pass
        
def draw(screen, populations):
    global man_sprite
    
    screen.fill((255, 255, 255)) 
    
    all_units = []
    for p in populations:
        all_units+=p.units
        
    all_units.sort(key=lambda unit: unit.position[Y])
        
    for unit in all_units:
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
def initialize_population(pop_center):
    new_pop = pop.Population()
    
    units = []
    unit_man_sprite = man_sprite.copy()
    recolor_sprite(unit_man_sprite)
        
    for i in range(10):
        new_unit = pop.Unit(new_pop)
        new_unit.position=[pop_center[X]+randint(0,size[X]/5), pop_center[Y]+randint(0,size[Y]/5)]
        new_unit.sprite=unit_man_sprite
        
        units.append( new_unit )
        
    
    new_pop.units = units
    return new_pop

pop1 = initialize_population([size[X]/5,size[Y]/2])
pop2 = initialize_population([4*size[X]/5,size[Y]/2])
pop1.other_populations.append(pop2)
pop2.other_populations.append(pop1)

populations = [pop1, pop2]

## Main game loop ##
nloop = 0
while done == False:
    
    # inputs
    handle_input_events()
    
    # update state
    for p in populations:
        p.act()
    
    #update(all_units)
    
    # screen draw
    draw(screen, populations)
     
    # run at X fps
    clock.tick(5)
    
    #pygame.image.save(screen, "screenshot%02d.tga" % nloop)
    nloop+=1
 
# close the window and quit
pygame.quit()
