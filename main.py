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
        self.velocitymult = 0.15
        self.brakerate = 0.95
        self.maxspeed = 20
        self.xvelocity = 0
        self.yvelocity = 0
        self.direction = 90
        self.rotatespeed = 5
        self.point1dist = 10
        self.point2dist = 10
        self.point3dist = 20
        self.firecooldown = 5

    def leftturn(self):
        self.direction += self.rotatespeed
        if self.direction > 360:
            self.direction -= 360

    def rightturn(self):
        self.direction -= self.rotatespeed
        if self.direction <= 0:
            self.direction += 360

    def thrust(self):
        referenceangle, xquad, yquad = findreferneceangle(self.direction)
        self.xvelocity += (math.cos(math.radians(referenceangle)) * xquad * self.velocitymult)
        if abs(self.xvelocity) > self.maxspeed:
            if self.xvelocity > 0:
                self.xvelocity = 20
            if self.xvelocity < 0:
                self.xvelocity = -20
        self.yvelocity -= (math.sin(math.radians(referenceangle)) * yquad * self.velocitymult)
        if abs(self.yvelocity) > self.maxspeed:
            if self.yvelocity > 0:
                self.yvelocity = 20
            if self.yvelocity < 0:
                self.yvelocity = -20

    def updatelocation(self):
        self.x += self.xvelocity
        self.y += self.yvelocity
        if self.firecooldown > 0:
            self.firecooldown -= 1
        #Warp if go off Screen
        if self.x < -20:
            self.x = 820
        if self.x > 820:
            self.x = -20
        if self.y < -20:
            self.y = 820
        if self.y > 820:
            self.y = -20

    def brake(self):
            self.xvelocity *= self.brakerate
            self.yvelocity *= self.brakerate

    def fire(self, bulletlist):
        #Only Fire of Cooldown is 0
        if self.firecooldown == 0:
            referenceangle, xquad, yquad = findreferneceangle(self.direction)#Find the Reference angle and Quadrant
            xvelocity = math.cos(math.radians(referenceangle)) * (self.point3dist - 4) * xquad#Find Speed
            yvelocity = math.sin(math.radians(referenceangle)) * (self.point3dist - 4) * yquad
            pointx = self.x + xvelocity#Determine the Location of X and Y of points
            pointy = self.y - yvelocity
            bulletlist.append(bullet((1 * xvelocity), (-1 * yvelocity), pointx, pointy))
            self.firecooldown = 5
            return bulletlist
        return bulletlist

#Bullets shot from Player
class bullet:
    def __init__(self, xvelocity, yvelocity, x, y):
        self.xvelocity = xvelocity
        self.yvelocity = yvelocity
        self.x = x
        self.y = y
        self.livecount = 60

    def updatelocation(self):
        self.x += self.xvelocity
        self.y += self.yvelocity

#Asteroid
class asteroid:
    def __init__(self, size, xvelocity, yvelocity, x, y):
        self.size = size
        self.xvelocity = xvelocity
        self.yvelocity = yvelocity
        self.x = x
        self.y = y

    def updatelocation(self):
        self.x += self.xvelocity
        self.y += self.yvelocity

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
        leftpressed = False
        rightpressed = False
        thrusting = False
        braking = False
        firing = False
        bulletlist = []
        asteroidlist = []
        spawnchance = 50
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
                elif event.type == pygame.KEYDOWN:
                    #Left Arrow
                    if event.key == pygame.K_LEFT:
                        leftpressed = True
                        rightpressed = False
                    #Right Arrow
                    elif event.key == pygame.K_RIGHT:
                        leftpressed = False
                        rightpressed = True
                    #Up Arrow
                    elif event.key == pygame.K_UP:
                        thrusting = True
                    #Down Arrow
                    elif event.key == pygame.K_DOWN:
                        braking = True
                    #Space
                    elif event.key == pygame.K_SPACE:
                        firing = True
                elif event.type == pygame.KEYUP:
                    #Left Arrow
                    if event.key == pygame.K_LEFT:
                        leftpressed = False
                    #Right Arrow
                    elif event.key == pygame.K_RIGHT:
                        rightpressed = False
                    #Up Arrow
                    elif event.key == pygame.K_UP:
                        thrusting = False
                    #Down Arrow
                    elif event.key == pygame.K_DOWN:
                        braking = False
                    #Space
                    elif event.key == pygame.K_SPACE:
                        firing = False

            #Cap FPS to 30
            clock.tick(30)

            #Do Calculations
            spawnchance, bulletlist, asteroidlist = calculate(screen, background_colour, spawnchance, asteroidlist, character, leftpressed, rightpressed, thrusting, braking, firing, bulletlist, tickcounter)
            tickcounter += tickspeed

def calculate(screen, background_colour, spawnchance, asteroidlist, character, leftpressed, rightpressed, thrusting, braking, firing, bulletlist, tickcounter):
    screen.fill(background_colour)
    #Increment Spawn Chance Occasionally
    if tickcounter % 300 == 0:
        spawnchance += 5

    #Spawn Asteroids Occasionally
    if tickcounter % 30 == 0:
        if random.randrange(0, 100) < spawnchance:
            #Spawn on Random Side
            side = random.randrange(0, 4)
            if side == 0:
                asteroidlist.append(asteroid(20, random.uniform(-1, 1), random.uniform(-1, 1), random.randrange(-20, 820), -20))
            if side == 1:
                asteroidlist.append(asteroid(20, random.uniform(-1, 1), random.uniform(-1, 1), random.randrange(-20, 820), 820))
            if side == 2:
                asteroidlist.append(asteroid(20, random.uniform(-1, 1), random.uniform(-1, 1), -20, random.randrange(-20, 820)))
            if side == 3:
                asteroidlist.append(asteroid(20, random.uniform(-1, 1), random.uniform(-1, 1), 820, random.randrange(-20, 820)))

    #Calculate Movement
    if leftpressed:
        character.leftturn()
    if rightpressed:
        character.rightturn()
    if thrusting:
        character.thrust()
    if braking:
        character.brake()
    if firing:
        bulletlist = character.fire(bulletlist)

    #Update Objects
    character.updatelocation()
    for bullet in bulletlist:
        bullet.updatelocation()
        bullet.livecount -= 1
        if bullet.livecount == 0:
            bulletlist.remove(bullet)
        #Check for Out Of Bounds
        if bullet.x < -20:
            bullet.x = 820
        if bullet.x > 820:
            bullet.x = -20
        if bullet.y < -20:
            bullet.y = 820
        if bullet.y > 820:
            bullet.y = -20
        pygame.draw.circle(screen, (255, 255, 255), (bullet.x, bullet.y), 2)
    for asteroidobject in asteroidlist:
        asteroidobject.updatelocation()
        #Check for Out Of Bounds
        if asteroidobject.x < -20:
            asteroidobject.x = 820
        if asteroidobject.x > 820:
            asteroidobject.x = -20
        if asteroidobject.y < -20:
            asteroidobject.y = 820
        if asteroidobject.y > 820:
            asteroidobject.y = -20
        pygame.draw.circle(screen, (128, 128, 128), (asteroidobject.x, asteroidobject.y), asteroidobject.size)

    #Draw Player
    #How far is each point from the center point
    point1arm = character.direction + 135
    if point1arm > 360:
        point1arm -= 360
    point2arm = character.direction - 135
    if point2arm <= 0:
        point2arm += 360

    #Calculate Point 1
    referenceangle, xquad, yquad = findreferneceangle(point1arm)#Find the Reference angle and Quadrant
    point1x = character.x + (math.cos(math.radians(referenceangle)) * character.point1dist * xquad)#Determine the Location of X and Y of points
    point1y = character.y - (math.sin(math.radians(referenceangle)) * character.point1dist * yquad)

    #Calculate Point 2
    referenceangle, xquad, yquad = findreferneceangle(point2arm)#Find the Reference angle and Quadrant
    point2x = character.x + (math.cos(math.radians(referenceangle)) * character.point2dist * xquad)#Determine the Location of X and Y of points
    point2y = character.y - (math.sin(math.radians(referenceangle)) * character.point2dist * yquad)

    #Calculate Point 3
    referenceangle, xquad, yquad = findreferneceangle(character.direction)#Find the Reference angle and Quadrant
    point3x = character.x + (math.cos(math.radians(referenceangle)) * character.point3dist * xquad)#Determine the Location of X and Y of points
    point3y = character.y - (math.sin(math.radians(referenceangle)) * character.point3dist * yquad)

    #Draw Player
    playercollide = pygame.draw.polygon(screen, (255, 255, 255), ((point1x, point1y), (point2x, point2y), (point3x, point3y)))

    pygame.display.update()

    return spawnchance, bulletlist, asteroidlist

def findreferneceangle(angle):
    #Find the Reference Angle
    if angle > 0 and angle <= 90:
        #Quadrant 1
        referenceangle = angle
        xquad = 1
        yquad = 1
    elif angle  > 90 and angle <= 180:
        #Quadrant 2
        referenceangle = 180 - angle
        xquad = -1
        yquad = 1
    elif angle > 180 and angle <= 270:
        #Quadrant 3
        xquad = -1
        yquad = -1
        referenceangle = angle - 180
    elif angle > 270 and angle <= 360:
        #Quadrant 4
        xquad = 1
        yquad = -1
        referenceangle = 360 - angle

    return referenceangle, xquad, yquad

#Call main() to Start Program
main()