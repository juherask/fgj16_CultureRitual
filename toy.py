import pygame
 
pygame.init()
size = [640, 480]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Culture Ritual')
clock = pygame.time.Clock()
 
def update():
    # clear the screen before drawing
    screen.fill((255, 255, 255)) 
	
	# display whats drawn. this might change.
    pygame.display.update()
    
def input_handler():
	pass

done = False
while done == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Game logic
 
    # screen draw
    update()
	 
    # run at 20 fps
    clock.tick(20)
 
# close the window and quit
pygame.quit()
