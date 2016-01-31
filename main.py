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
level = 0
sounds = True
music = True

def load_assets():
    global man_sprite
    global man_frame_key
    man_sprite = pygame.image.load('assets/zealot.png').convert_alpha()
    button_sprite = pygame.image.load('assets/button.png').convert_alpha()
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

def draw_ui(screen, buttons):
    for btn in buttons:
        # button is 3-tuple (color, rect, text)
        
        pygame.draw.rect(screen, ...)
        #pygame.font.render()
        myfont.render()

def draw_sprites(screen, all_units):
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


def show_level_start_window(screen,levelNo):
    #Display the start-of-level dialog box that corresponds to the current level
    print("Displaying level start window for level "+str(level))
    #(startWidth,startHeight) = (300,200)
    #screen = pygame.display.set_mode((startWidth, startHeight))
    pygame.display.set_caption('Little voice inside your head')
    print(dir(pygame.display))
    if sounds == True:
        print("Playing level start sound")
    soundLib = ["firstLevelIntro.mp3",
                "secondLevelIntro.mp3",
                "thirdLevelIntro.mp3"]
    """
    villageNames = ["Onagh",
                    "Tuurum",
                    "Erukun",
                    "Tikka",
                    "Wakkadokko",
                    "Illur",
                    "Tooh",
                    "Odok",
                    "Aaru",
                    "Nukku",
                    "Kaala",
                    "Offodok",
                    "Sellak",
                    "Piir",
                    "Eknaa",
                    "Ollo",
                    "Qir"]
    """

    missionStrings = [["The village of Tooh must grow.","The people are afraid, they need ","the feeling of safety again."],
                      ["The rival village of Wakkadokko"," have committed ","unspeakable acts. The only way ","to solve this is ","violence.","They must not be allowed to survive.","Do what must be done."],
                      ["The people of Eknaa are,"," breeding without any restraint!","No good can come from this.","Make it stop."," Make them know."]]

    defaultButtonWidth = screen.get_width()*0.1
    defaultButtonHeight = screen.get_height()*0.03

    greyTuple = (30,30,30)

    posXRel = screen.get_width()
    posYRel = screen.get_height()

    buttonDict = {"levelStart":[pygame.draw.rect(screen,greyTuple,(posXRel/2,posYRel*-0.9,defaultButtonWidth,defaultButtonHeight)),"Let it begin"],
                  "levelEnd":[pygame.draw.rect(screen,greyTuple,(posXRel*0.3,posYRel*-0.6,defaultButtonWidth,defaultButtonHeight)),"It is done"],
                  "Human Sacrifice":[pygame.draw.rect(screen,greyTuple,(posXRel*0.5,posYRel*-0.3,defaultButtonWidth,defaultButtonHeight)),"Human Sacrifice"],
                  "Animal Sacrifice":[pygame.draw.rect(screen,greyTuple,(posXRel*0.7,posYRel*-0.75,defaultButtonWidth,defaultButtonHeight)),"Animal Sacrifice"],
                  "Psychedelics":[pygame.draw.rect(screen,greyTuple,(posXRel*0.1,posYRel*-0.1,defaultButtonWidth,defaultButtonHeight)),"Psychedelics"],
                  "Food Sacrifice":[pygame.draw.rect(screen,greyTuple,(posXRel*0.3,posYRel*-0.9,defaultButtonWidth,defaultButtonHeight)),"Food Sacrifice"],
                  "Music":[pygame.draw.rect(screen,greyTuple,(posXRel*0.3,posYRel*-0.6,defaultButtonWidth,defaultButtonHeight)),"Music"],
                  "Social Isolation":[pygame.draw.rect(screen,greyTuple,(posXRel*0.3,posYRel*-0.6,defaultButtonWidth,defaultButtonHeight)),"Social Isolation"]}
    

    textMeasPosHeight = screen.get_height()/2
    
    for stringBit in missionStrings[levelNo]:
        text_surface = myfont.render(stringBit, False, (255,0,0))
        
        #print(dir(text_surface))
        textMeasLength = text_surface.get_width()
        textMeasPosHeight -= text_surface.get_height()

        

        #button = Button() #Button class is created
        #buttonWidthAdjust = button.get_width()/2
        #button.setCords(screen.get_width()/2-buttonWidthAdjust)

        

        screen.blit(text_surface,(screen.get_width()/2-textMeasLength/2,screen.get_height()/2-textMeasPosHeight))   

    
    
    pygame.display.flip()
    dir(pygame.display)

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
    
    

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

pygame.display.set_caption('Culture Ritual')
if music == True:
    print("Starting music")
    #play.music(-1)

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

#Intro window loop
show_level_start_window(screen,2)
pygame.display.set_caption('Culture Ritual')
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
    draw_sprites(screen, all_units)
     
    # run at X fps
    clock.tick(15)
    
    pygame.image.save(screen, "screenshot%02d.tga" % nloop)
    nloop+=1
 
# close the window and quit
pygame.quit()
