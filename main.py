#Asteroids

#Import Libraries
import pygame
import random
pygame.init()

#Functions
def main():
    #Create Display
    (width, height) = (800, 800)
    background_colour = (0, 0, 0)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Asteroids")
    #This is to Reset after a Gameover
    cont = True
    while cont:
        clock = pygame.time.Clock()
        tickcounter = 0
        tickspeed = 1

        #Main Program Loop
        running = True
        while running:
            #Check for User Input
            for event in pygame.event.get():
                #Detected User Clicked on X
                if event.type == pygame.QUIT:
                    running = False
                    cont = False
                    #Detected Mouse Click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #Left Click
                    if event.button == 1:
                        pass

            #Cap FPS to 30
            clock.tick(30)

            tickcounter += tickspeed

            #Update Screen
            draw(screen, background_colour)

def draw(screen, background_colour):
    screen.fill(background_colour)

    pygame.display.update()

#Call main() to Start Program
main()