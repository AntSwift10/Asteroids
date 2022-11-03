#Asteroids

#Import Libraries
import pygame
import random
pygame.init()

#Classes
#Player Character
class player:
    def __init__(self):
        self.x = 400
        self.y = 400
        self.xvelocity = 0
        self.yvelocity = 0
        self.direction = 360

    def leftturn(self):
        self.direction -= 1
        if self.direction < 0:
            self.direction = 360

    def rightturn(self):
        self.direction += 1
        if self.direction > 360:
            self.direction = 0

    def thrust(self):
        #Make this thrust the player in the direction they are facing with math
        pass

#Asteroid
class asteroid:
    def __init__(self, size):
        self.size = size

    def shatter(self):
        #Create more, Smaller Asteroids
        pass

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
        #Create Player
        character = player()

        #Create Clock
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

            #Do Calculations
            calculate(screen, background_colour, character)
            tickcounter += tickspeed

def calculate(screen, background_colour, character):
    screen.fill(background_colour)

    #Draw Player
    playercollide = pygame.draw.polygon(screen, (255, 255, 255), ((character.x - 10, character.y - 10), (character.x + 10, character.y - 10), (character.x, character.y - 40)))

    pygame.display.update()

#Call main() to Start Program
main()