import pygame
from random import random, randint
from collections import OrderedDict
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
man_frame_key = None

def load_assets():
    global man_sprite
    global man_frame_key
    man_sprite = pygame.image.load('assets/zealot.png').convert_alpha()
    man_frame_key = OrderedDict([
        ("idle", (0.1, [])),
        ("walk_s",(0.5, [])),
        ("walk_n",(0.5, [])),
        ("walk_w",(0.5, [])),
        ("walk_e",(0.5, []))])
    for cycle, key in enumerate(man_frame_key.keys()):
        for frame in range(4):
            r = pygame.Rect( frame*20, cycle*30, 20, 30 )
            man_frame_key[key][1].append(r)

def recolor_sprite(sprite):
    pixels = pygame.surfarray.pixels2d( sprite )
    #print hex(pixels[0][0] & (2**32-1))
    #print hex(pixels[15][25] & (2**32-1))
    #print hex(pixels[25][15] & (2**32-1))
    #print(pixels[15][25], hex(pixels[15][25]))
    
    a = 255
    r,g,b = randint(70,200),randint(70,200),randint(70,200)
    base_shirt_color = a*256**3+r*256**2 + g*256 + b
    light_shirt_color = a*256**3+(r+25)*256**2 + (g+25)*256 + (b+25)
    dark_shirt_color = a*256**3+(r-50)*256**2 + (g-50)*256 + (b-50)
    
    for x in range(len(pixels)):
        for y in range(len(pixels[0])):
            if pixels[x][y]==color_bit_conversion(0xFF9B4C16):
                pixels[x][y] = color_bit_conversion(base_shirt_color)
            if pixels[x][y]==color_bit_conversion(0xFFAF7F5E):
                pixels[x][y] = color_bit_conversion(light_shirt_color)
            if pixels[x][y]==color_bit_conversion(0xFF663E23):
                pixels[x][y] = color_bit_conversion(dark_shirt_color)

def update(units):
    pass
        
def draw(screen, all_units):
    global man_frame_key
    
    # Todo: some base graphic
    screen.fill((29, 54, 75)) 
    
    all_units.sort(key=lambda unit: unit.position[Y])
    for unit in all_units:
        anim = None
        if unit.dv == [0.0,0.0]:
            anim = "idle"
        elif abs(unit.dv[X])>abs(unit.dv[Y]):
            if unit.dv[X]<0:
                anim = "walk_w"
            else:
                anim = "walk_e"
        else:
            if unit.dv[Y]<0:
                anim = "walk_n"
            else:
                anim = "walk_s"
            
        unit.sprite.set_clip( man_frame_key[anim][1][int(unit.anim_frame)] )
        sprite_frame = unit.sprite.subsurface(unit.sprite.get_clip())
        screen.blit(sprite_frame, unit.position)
        
        unit.anim_frame+=1.0
        if unit.anim_frame>3.5:
            unit.anim_frame = 0
        
    
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
def initialize_population(pop_size, pop_center, all_units_list):
    global man_sprite
    new_pop = pop.Population(all_units_list)
    
    unit_man_sprite = man_sprite.copy()
    recolor_sprite(unit_man_sprite)
        
    for i in range(pop_size):
        new_unit = pop.Unit(new_pop)
        new_unit.position=[pop_center[X]+randint(0,size[X]/5), pop_center[Y]+randint(0,size[Y]/5)]
        new_unit.sprite=unit_man_sprite
        all_units_list.append( new_unit )
        
    return new_pop

all_units = []
pop1 = initialize_population(12, [size[X]/5,size[Y]/2], all_units)
pop2 = initialize_population(7, [3*size[X]/5,size[Y]/2], all_units)
pop3 = initialize_population(9, [size[X]/2,size[Y]/2+50], all_units)
populations = [pop1, pop2, pop3]

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
    draw(screen, all_units)
     
    # run at X fps
    clock.tick(15)
    
    pygame.image.save(screen, "screenshot%02d.tga" % nloop)
    nloop+=1
 
# close the window and quit
pygame.quit()
