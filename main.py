import pygame
from random import random, randint, choice
from collections import OrderedDict
from numpy import int32, int64
import platform
from intro import show_level_start_window
if platform.architecture()[0]=='32bit':
    color_bit_conversion = int64
else:
    color_bit_conversion = int32

#import os, sys
#sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import pop
from actions import influence_population

# ~DEFINES
X = 0
Y = 1
AEGING_SPEED = 0.01 #how quickly population grows, how quickly cooldowns inc

COLOR_GRAY = (30,30,30)

# Globals, UGLY!
done = False
man_sprite = None
man_frame_key = None
all_units = []
populations = []
active_population_idx = 0
level = 0
sounds = True
music = True
sound_effects = {}

def load_assets():
    global man_sprite
    global man_frame_key
    man_sprite = pygame.image.load('assets/zealot.png').convert_alpha()
    man_frame_key = OrderedDict([
        ("idle", (0.1, [])),
        ("walk_s",(0.5, [])),
        ("walk_n",(0.5, [])),
        ("walk_w",(0.5, [])),
        ("walk_e",(0.5, [])),
        ("poof",(0.2, [])),
        ("die",(0.2, [])),
        ("stab",(0.2, [])),
        ("Dance",(0.2, [])),
        ("Food sacrifice",(0.2, [])),
        ("Animal sacrifice",(0.2, [])),
        ("Psychedelics",(0.2, [])),
        ("Social isolation",(0.2, []))
    ])
    for cycle, key in enumerate(man_frame_key.keys()):
        for frame in range(6):
            r = None
            if key == "Social isolation":
                r = pygame.Rect( 2*20, 6*30, 20, 30 )
            else:
                r = pygame.Rect( frame*20, cycle*30, 20, 30 )
            man_frame_key[key][1].append(r)
            
    # To do: load sound effects and music
    pygame.mixer.music.load('assets/BackroundMusic.wav')
    pygame.mixer.music.play(-1)
    
    sound_effects["Music"] = None
    sound_effects["Dance"] = None
    sound_effects["Psychedelics"] = None
    sound_effects["Social isolation"] = None
    sound_effects["Animal sacrifice"] = None
    sound_effects["Human sacrifice"] = None
    sound_effects["Plant sacrifice"] = None
    sound_effects["Food sacrifice"] = None
    
    
            
    

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
    
    
def update(populations, all_unitsh):
    # age
    for u in all_units:
        # procreation cooldown doubles as age
        u.procreate_cooldown=max(0.0, u.procreate_cooldown-AEGING_SPEED)
        u.meet_cooldown=max(0.0, u.meet_cooldown-AEGING_SPEED)
    
    for p in populations:
        p.act()

def draw_ui(screen, buttons, myfont):
    
    for btn in buttons:
        # button is 3-tuple (color, rect, text)
        pygame.draw.rect(screen, btn[0], btn[1])
        text_surface = myfont.render(btn[2], False, (255,0,0))
        screen.blit(text_surface,btn[1])   


def draw_sprites(screen, all_units):
    global man_frame_key
    
    # Todo: some base graphic
    screen.fill((29, 54, 75)) 
    
    all_units.sort(key=lambda unit: unit.position[Y])
    for unit in all_units:
        anim = None
        
        # Standard reactive actions
        if unit.action_anim_key == None:
            if unit.dv[X]<0.001 and unit.dv[Y]<0.001:
                if unit.procreate_cooldown>1.0:
                    anim = "poof"
                else:
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
        # initial actions
        else:
            anim = unit.action_anim_key
            
            unit.action_anim_cooldown-=AEGING_SPEED
            if unit.action_anim_cooldown< 0.0:
                # animation done, ok
                unit.action_anim_cooldown = 0.0
                unit.action_anim_key = None
                
                
        unit.sprite.set_clip( man_frame_key[anim][1][int(unit.anim_frame)] )
        sprite_frame = unit.sprite.subsurface(unit.sprite.get_clip())
        screen.blit(sprite_frame, unit.position)
        
        unit.anim_frame+=man_frame_key[anim][0]
        if unit.anim_frame>3.5:
            if anim == "poof":
                unit.anim_frame = 3
            else:
                unit.anim_frame = 0
    
def do_ritual(ritual_key):
    global all_units
    global populations
    global active_population_idx
    global man_frame_key
    
    active_population = populations[active_population_idx]
    
    # rituals affect to the mood of the population and change how 
    #  they behave
    influence_population(active_population, ritual_key)
        
    units_in_active_pop = [unit for unit in all_units if
        (unit.population == active_population and
        unit.procreate_cooldown<=1.0 and # children do not do rituals
        unit.action_anim_cooldown==0.0)]
    if len(units_in_active_pop)==0:
        print("WARNING: no units available for a ritual in the population")
        return
    
    
    
    if ritual_key in man_frame_key.keys():
        victim = choice(units_in_active_pop)
        victim.action_anim_key = ritual_key
        victim.action_anim_cooldown = 2.0 # duration of the anim (in age units).
    elif ritual_key == "Human sacrifice":
        for u in units_in_active_pop:
            # someone dies
            if active_population.kill_whomever_is_close(unit)!=None:
                break
		
    else:
        print("ERROR: unknown ritual", ritual_key)
        
def handle_input_events(buttons):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on_esc_pressed()
            
        elif event.type == pygame.KEYDOWN:
            global populations
            global active_population_idx
            if event.key == pygame.K_p:
                populations[active_population_idx].propensity_library["fear"]=100
                populations[active_population_idx].propensity_library["responsibility"]=50
            
            if event.key == pygame.K_1:
                active_population_idx = 0
            if event.key == pygame.K_2:
                active_population_idx = 1
            if event.key == pygame.K_3:
                active_population_idx = 2
                
            if event.key == pygame.K_z:
                do_ritual("Dance")
            if event.key == pygame.K_x:
                do_ritual("Human sacrifice")
            if event.key == pygame.K_c:
                do_ritual("Food sacrifice")
            if event.key == pygame.K_v:
                do_ritual("Animal sacrifice") 
            if event.key == pygame.K_b:
                do_ritual("Psychedelics")
            if event.key == pygame.K_n:
                do_ritual("Social isolation") 
            
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for btn in buttons:
                #[COLOR_GRAY,pygame.Rect(posXRel*0.5,posYRel*0.3,defaultButtonWidth,defaultButtonHeight),"Human Sacrifice"],
                if btn[1].collidepoint(pos):
                    print(btn[2])
                    do_ritual(btn[2].strip()) 
                    break
                
def on_esc_pressed():
    global done
    done = True

def show_level_end_window(level):
    #Display the end-of-level dialog box that corresponds to the current level
    print("Displaying the level end window for level "+str(level))

## Pygame initialization ##
pygame.init()
size = [640, 480]
screen = pygame.display.set_mode(size)

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont("Comic Sans MS", 30)
ritualfont = pygame.font.SysFont("Times New Roman", 18)

pygame.display.set_caption('Culture Ritual')
if music == True:
    print("Starting music")
    #play.music(-1)

clock = pygame.time.Clock()

load_assets()

populations.append(initialize_population(12, [size[X]/5,size[Y]/2], all_units))
populations.append(initialize_population(7, [3*size[X]/5,size[Y]/2], all_units))
populations.append(initialize_population(9, [size[X]/2,size[Y]/2+50], all_units))

#Intro window loop
show_level_start_window(screen,2)
pygame.display.set_caption('Culture Ritual')
## Main game loop ##
nloop = 0

defaultButtonWidth = screen.get_width()*0.2
defaultButtonHeight = screen.get_height()*0.05
posXRel = screen.get_width()
posYRel = screen.get_height()
ritual_buttons = [
    [COLOR_GRAY,pygame.Rect(posXRel*0.2,posYRel*0.1,defaultButtonWidth,defaultButtonHeight)," Human sacrifice"],
    [COLOR_GRAY,pygame.Rect(posXRel*0.1,posYRel*0.2,defaultButtonWidth,defaultButtonHeight)," Animal sacrifice"],
    [COLOR_GRAY,pygame.Rect(posXRel*0.2,posYRel*0.3,defaultButtonWidth,defaultButtonHeight)," Psychedelics"],
    [COLOR_GRAY,pygame.Rect(posXRel*0.6,posYRel*0.1,defaultButtonWidth,defaultButtonHeight), "Food sacrifice"],
    [COLOR_GRAY,pygame.Rect(posXRel*0.7,posYRel*0.2,defaultButtonWidth,defaultButtonHeight)," Music"],
    [COLOR_GRAY,pygame.Rect(posXRel*0.6,posYRel*0.3,defaultButtonWidth,defaultButtonHeight)," Social isolation"]
]

while done == False:
    # inputs
    handle_input_events(ritual_buttons)
    
    # update state
    update(populations, all_units)

    # screen draw
    draw_sprites(screen, all_units)
    draw_ui(screen, ritual_buttons, ritualfont)
    pygame.display.update()
     
    # run at X fps
    clock.tick(15)
    
    #pygame.image.save(screen, "screenshot%02d.tga" % nloop)
    nloop+=1
 
# close the window and quit
pygame.quit()
