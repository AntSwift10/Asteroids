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
        self.firingspeedpowerups = 0
        self.multishotpowerups = 0
        self.rangepowerups = 0
        match self.rangepowerups:
            case 0:
                self.range = 5
            case 1:
                self.range = 15
            case 2:
                self.range = 30
            case 3:
                self.range = 60
            case _:
                self.range = 100
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
        match self.firingspeedpowerups:
            case 0:
                self.maxcooldown = 20
            case 1:
                self.maxcooldown = 10
            case 2:
                self.maxcooldown = 5
            case 3:
                self.maxcooldown = 2
            case _:
                self.maxcooldown = 1
        self.firecooldown = self.maxcooldown

    def fire(self, bulletlist):
        #Only Fire if Cooldown is 0
        if self.firecooldown == 0:
            #Fire Based on Number of Power Ups
            match self.multishotpowerups:
                case 0:
                    bulletlist = firebullet(self.direction, self.x, self.y, self.point3dist, bulletlist, self.range)
                    self.firecooldown = self.maxcooldown
                    return bulletlist
                case 1:
                    bulletlist = firebullet(self.direction - 2, self.x, self.y, self.point3dist, bulletlist, self.range)
                    bulletlist = firebullet(self.direction + 2, self.x, self.y, self.point3dist, bulletlist, self.range)
                    self.firecooldown = self.maxcooldown
                    return bulletlist
                case 2:
                    bulletlist = firebullet(self.direction - 3, self.x, self.y, self.point3dist, bulletlist, self.range)
                    bulletlist = firebullet(self.direction, self.x, self.y, self.point3dist, bulletlist, self.range)
                    bulletlist = firebullet(self.direction + 3, self.x, self.y, self.point3dist, bulletlist, self.range)
                    self.firecooldown = self.maxcooldown
                    return bulletlist
                case 3:
                    bulletlist = firebullet(self.direction - 6, self.x, self.y, self.point3dist, bulletlist, self.range)
                    bulletlist = firebullet(self.direction - 2, self.x, self.y, self.point3dist, bulletlist, self.range)
                    bulletlist = firebullet(self.direction + 2, self.x, self.y, self.point3dist, bulletlist, self.range)
                    bulletlist = firebullet(self.direction + 6, self.x, self.y, self.point3dist, bulletlist, self.range)
                    self.firecooldown = self.maxcooldown
                    return bulletlist
                case _:
                    bulletlist = firebullet(self.direction - 6, self.x, self.y, self.point3dist, bulletlist, self.range)
                    bulletlist = firebullet(self.direction - 3, self.x, self.y, self.point3dist, bulletlist, self.range)
                    bulletlist = firebullet(self.direction, self.x, self.y, self.point3dist, bulletlist, self.range)
                    bulletlist = firebullet(self.direction + 3, self.x, self.y, self.point3dist, bulletlist, self.range)
                    bulletlist = firebullet(self.direction + 6, self.x, self.y, self.point3dist, bulletlist, self.range)
                    self.firecooldown = self.maxcooldown
                    return bulletlist
        return bulletlist

    def updatepowerlevel(self):
        match self.rangepowerups:
            case 0:
                self.range = 5
            case 1:
                self.range = 15
            case 2:
                self.range = 30
            case 3:
                self.range = 60
            case _:
                self.range = 100
        match self.firingspeedpowerups:
            case 0:
                self.maxcooldown = 20
            case 1:
                self.maxcooldown = 10
            case 2:
                self.maxcooldown = 5
            case 3:
                self.maxcooldown = 2
            case _:
                self.maxcooldown = 1

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

#Bullets shot from Player
class bullet:
    def __init__(self, xvelocity, yvelocity, x, y, livecount):
        self.xvelocity = xvelocity
        self.yvelocity = yvelocity
        self.x = x
        self.y = y
        self.livecount = livecount
        self.size = 2

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
        self.mask = None

    def updatelocation(self):
        self.x += self.xvelocity
        self.y += self.yvelocity

    def shatter(self, asteroidlist, poweruplist):
        #Create more, Smaller Asteroids
        if self.size > 15:
            n = 0
            while n < random.randrange(2, 4):
                asteroidlist.append(asteroid(self.size * random.uniform(0.5, 0.6), random.uniform(-1, 1), random.uniform(-1, 1), self.x + random.uniform(-self.size / 2, self.size / 2), self.y + random.uniform(-self.size / 2, self.size / 2)))
                n += 1
        #Chance to Create Powerups
        number = random.randrange(100)
        if number <= 2:
            poweruplist.append(powerup(self.x, self.y, number))
        return asteroidlist, poweruplist

#Power Ups
class powerup:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.size = 10
        self.mask = None
        self.xvelocity = random.uniform(-1, 1)
        self.yvelocity = random.uniform(-1, 1)
        if type == 0: #Multi Shot
            self.colour = (255, 0, 0)
        if type == 1: #Fire Rate
            self.colour = (0, 255, 0)
        if type == 2:#Range
            self.colour = (0, 0, 255)

    def updatelocation(self):
        self.x += self.xvelocity
        self.y += self.yvelocity

#Functions
def main():
    #Create Display
    (width, height) = (800, 800)
    background_colour = (0, 0, 0)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Asteroids")
    font = pygame.font.SysFont("Cambria.ttc", 30)
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
        poweruplist = []
        spawnchance = 5
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
            spawnchance, bulletlist, asteroidlist, cont, running, poweruplist = calculate(screen, background_colour, spawnchance, asteroidlist, character, leftpressed, rightpressed, thrusting, braking, firing, bulletlist, font, cont, running, tickcounter, poweruplist)
            tickcounter += tickspeed

def calculate(screen, background_colour, spawnchance, asteroidlist, character, leftpressed, rightpressed, thrusting, braking, firing, bulletlist, font, cont, running, tickcounter, poweruplist):
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
                asteroidlist.append(asteroid(random.randrange(20, 40), random.uniform(-1, 1), random.uniform(-1, 1), random.randrange(-40, 840), -40))
            if side == 1:
                asteroidlist.append(asteroid(random.randrange(20, 40), random.uniform(-1, 1), random.uniform(-1, 1), random.randrange(-40, 840), 840))
            if side == 2:
                asteroidlist.append(asteroid(random.randrange(20, 40), random.uniform(-1, 1), random.uniform(-1, 1), -40, random.randrange(-40, 840)))
            if side == 3:
                asteroidlist.append(asteroid(random.randrange(20, 40), random.uniform(-1, 1), random.uniform(-1, 1), 840, random.randrange(-40, 840)))

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
        collision = False
        bullet.updatelocation()
        bullet.livecount -= 1
        #Check for Out Of Bounds
        if bullet.x < -20:
            bullet.x = 820
        if bullet.x > 820:
            bullet.x = -20
        if bullet.y < -20:
            bullet.y = 820
        if bullet.y > 820:
            bullet.y = -20
        #Check for Collision Detection
        for asteroidobject in asteroidlist:
            if math.sqrt(pow(abs(bullet.x - asteroidobject.x), 2) + pow(abs(bullet.y - asteroidobject.y), 2)) <= (bullet.size + asteroidobject.size):
                #Detected collision
                bulletlist.remove(bullet)
                asteroidobject.shatter(asteroidlist, poweruplist)
                asteroidlist.remove(asteroidobject)
                collision = True
                break
        if bullet.livecount == 0 and collision == False:
            bulletlist.remove(bullet)
        pygame.draw.circle(screen, (255, 255, 255), (bullet.x, bullet.y), bullet.size)
    for asteroidobject in asteroidlist:
        asteroidobject.updatelocation()
        #Check for Out Of Bounds
        if asteroidobject.x < -40:
            asteroidobject.x = 840
        if asteroidobject.x > 840:
            asteroidobject.x = -40
        if asteroidobject.y < -40:
            asteroidobject.y = 840
        if asteroidobject.y > 840:
            asteroidobject.y = -40
        #Draw and Create Masks for Collision Detection
        asteroidsurface = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.circle(asteroidsurface, (128, 128, 128), (50, 50), asteroidobject.size)
        screen.blit(asteroidsurface, (asteroidobject.x - 50, asteroidobject.y - 50))
        asteroidobject.mask = pygame.mask.from_surface(asteroidsurface)
    for powerupobject in poweruplist:
        powerupobject.updatelocation()
        if powerupobject.x < -20:
            powerupobject.x = 820
        if powerupobject.x > 820:
            powerupobject.x = -20
        if powerupobject.y < -20:
            powerupobject.y = 820
        if powerupobject.y > 820:
            powerupobject.y = -20
        powerupsurface = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.rect(powerupsurface, powerupobject.colour, (15, 15, powerupobject.size, powerupobject.size))
        screen.blit(powerupsurface, (powerupobject.x - 15, powerupobject.y - 15))
        powerupobject.mask = pygame.mask.from_surface(powerupsurface)

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
    playersurface = pygame.Surface((60, 60), pygame.SRCALPHA)
    pygame.draw.polygon(playersurface, (255, 255, 255), ((point1x + 30 - character.x, point1y + 30 - character.y), (point2x + 30 - character.x, point2y + 30 - character.y), (point3x + 30 - character.x, point3y + 30 - character.y)))
    screen.blit(playersurface, (character.x - 30, character.y - 30))

    #Create a Mask for Collision Detection
    mask_player = pygame.mask.from_surface(playersurface)

    #Player, Asteroid Collision Detection
    for asteroidobject in asteroidlist:
        offset = (asteroidobject.x - 50) - (character.x - 30), (asteroidobject.y - 50) - (character.y - 30)
        collision = mask_player.overlap(asteroidobject.mask, offset)
        if collision != None:
            cont, running = gameover(screen, font)

    #Player, Powerup Collision
    for powerupobject in poweruplist:
        offset = (powerupobject.x - 15) - (character.x - 30), (powerupobject.y - 15) - (character.y - 30)
        collision = mask_player.overlap(powerupobject.mask, offset)
        if collision != None:
            match powerupobject.type:
                case 0: #Multi Shot
                    character.multishotpowerups += 1
                case 1: #Fire Rate
                    character.firingspeedpowerups += 1
                case 2: #Range
                    character.rangepowerups += 1
            poweruplist.remove(powerupobject)
            character.updatepowerlevel()

    pygame.display.update()

    return spawnchance, bulletlist, asteroidlist, cont, running, poweruplist

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

def firebullet(angle, x, y, point3dist, bulletlist, livecount):
    if angle > 360:
        angle -= 360
    if angle <= 0:
        angle += 360
    referenceangle, xquad, yquad = findreferneceangle(angle)#Find the Reference angle and Quadrant
    xvelocity = math.cos(math.radians(referenceangle)) * (point3dist - 4) * xquad#Find Speed
    yvelocity = math.sin(math.radians(referenceangle)) * (point3dist - 4) * yquad
    pointx = x + xvelocity#Determine the Location of X and Y of points
    pointy = y - yvelocity
    bulletlist.append(bullet((1 * xvelocity), (-1 * yvelocity), pointx, pointy, livecount))
    return bulletlist

def gameover(screen, font):
    bigfont = pygame.font.SysFont("Cambria.ttc", 100)
    quittext = font.render("Quit?", True, (255, 255, 255))
    continuetext = font.render("Try Again?", True, (255, 255, 255))
    gameovertext = bigfont.render("GAMEOVER", True, (255, 50, 50))
    quitbutt = pygame.draw.rect(screen, (255, 50, 50), (170, 472, 150, 75))
    continuebutt = pygame.draw.rect(screen, (255, 50, 50), (475, 472, 150, 75))
    #Game Over Loop
    running = True
    while running:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 50, 50), (475, 472, 150, 75))
        pygame.draw.rect(screen, (255, 50, 50), (170, 472, 150, 75))
        screen.blit(gameovertext, (200, 200))
        screen.blit(quittext, (220, 500))
        screen.blit(continuetext, (500, 500))
        #Check for User Input
        for event in pygame.event.get():
            #Detected User Clicked on X
            if event.type == pygame.QUIT:
                quit()
                #Detected Mouse Click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Left Click
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if quitbutt.collidepoint(pos):
                        quit()
                    elif continuebutt.collidepoint(pos):
                        return True, False
        
        pygame.display.update()

#Call main() to Start Program
main()