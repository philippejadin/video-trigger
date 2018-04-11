import sys, pygame, time
pygame.init()

size = width, height = 800, 600

black = 0, 0, 0
white = 255, 255, 255

#screen = pygame.display.set_mode(size)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)



'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            # If pressed key is ESC quit program
            if event.key == pygame.K_ESCAPE:
                sys.exit()
'''

for x in range(0, 3):
    screen.fill(black)
    pygame.display.flip()
    time.sleep(1)
    screen.fill(white)
    pygame.display.flip()
    time.sleep(1)