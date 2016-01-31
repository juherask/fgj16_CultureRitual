import pygame

COLOR_GRAY = (30,30,30)

pygame.font.init()
myfont = pygame.font.SysFont("Comic Sans MS", 30)

def show_level_start_window(screen,levelNo):
    #Display the start-of-level dialog box that corresponds to the current level
    print("Displaying level start window for level "+str(levelNo))
    #(startWidth,startHeight) = (300,200)
    #screen = pygame.display.set_mode((startWidth, startHeight))
    pygame.display.set_caption('Little voice inside your head')
    print(dir(pygame.display))
    #if sounds == True:
    #    print("Playing level start sound")
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
    posXRel = screen.get_width()
    posYRel = screen.get_height()

    buttonDict = [[COLOR_GRAY,(posXRel/2,posYRel*0.9,defaultButtonWidth,defaultButtonHeight),"Let it begin"],
                  [COLOR_GRAY,(posXRel*0.3,posYRel*0.6,defaultButtonWidth,defaultButtonHeight),"It is done"]]

    textMeasPosHeight = screen.get_height()/2
    
    for stringBit in missionStrings[levelNo]:
        text_surface = myfont.render(stringBit, False, (255,0,0))
        textMeasLength = text_surface.get_width()
        textMeasPosHeight -= text_surface.get_height()
        screen.blit(text_surface,(screen.get_width()/2-textMeasLength/2,screen.get_height()/2-textMeasPosHeight))   

    
    
    pygame.display.flip()
    dir(pygame.display)

    running = True
    while running:                
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.mouse.get_pressed()[0]:
                running = False
                
    
