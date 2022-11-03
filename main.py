#Asteroids

#Import Libraries
import pygame
import math
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
        self.direction = 45

    def leftturn(self):
        self.direction -= 3
        if self.direction <= 0:
            self.direction += 360

    def rightturn(self):
        self.direction += 3
        if self.direction > 360:
            self.direction -= 360

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
    #How far is each point from the center point
    point1dist = 10
    point1arm = character.direction + 135
    if point1arm > 360:
        point1arm -= 360
    point2dist = 10
    point2arm = character.direction - 135
    if point2arm <= 0:
        point2arm += 360
    point3dist = 40

    referenceangle = findreferneceangle(character.direction)

    #Calculate Point 3
    point3x = character.x + (math.cos(math.radians(referenceangle)) * point3dist)
    point3y = character.y - (math.sin(math.radians(referenceangle)) * point3dist)
    playercollide = pygame.draw.polygon(screen, (255, 255, 255), ((character.x - 10, character.y - 10), (character.x + 10, character.y - 10), (point3x, point3y)))

    pygame.display.update()

def findreferneceangle(angle):
    #Find the Reference Angle
    if angle > 0 and angle <= 90:
        #Quadrant 1
        referenceangle = angle
    elif angle  > 90 and angle <= 180:
        #Quadrant 2
        referenceangle = 180 - angle
    elif angle > 180 and angle <= 270:
        #Quadrant 3
        referenceangle = angle - 180
    elif angle > 270 and angle <= 360:
        #Quadrant 4
        referenceangle = 360 - angle

    return referenceangle

#Call main() to Start Program
main()