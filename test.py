import pygame, random, sys
from pygame.locals import *

pygame.init()

width = 640
height = 480


DISPLAYSURF = pygame.display.set_mode((width, height))
pygame.display.set_caption('It moves!')
pygame.mouse.set_visible(0)



class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.width = 50
        self.height = 25
        self.playerRect = None



    def update(self, event):
        if event.type == MOUSEMOTION:
            self.x, self.y = event.pos


        #get a new playerRect and draw it
        self.playerRect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.ellipse(DISPLAYSURF, RED, (self.playerRect), 3)


    def shotcheck(self, event):
        if event.type == KEYDOWN:
            if event.key == K_KP8:
                return (True, 'up')
            elif event.key == K_KP2:
                return (True, 'down')
            elif event.key == K_KP4:
                return (True, 'left')
            elif event.key == K_KP6:
                return (True, 'right')
            elif event.key == K_KP7:
                return (True, 'upleft')
            elif event.key == K_KP1:
                return (True, 'downleft')
            elif event.key == K_KP9:
                return (True, 'upright')
            elif event.key == K_KP3:
                return (True, 'downright')
            else:
                return (0, 0)



class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        #self.body = pygame.rect.Rect(self.x, self.y, 15, 15)
        self.speed = 5
        self.xmove = 0
        self.ymove = 0



    def update(self, event):
        self.x += self.speed
        if self.x > 350:
            self.speed *= -1
        elif self.x < 25:
            self.speed *= -1

        pygame.draw.rect(DISPLAYSURF, BLUE, (self.x, self.y, 15, 15), 4)



#pass it a directional value when fired based on the key
#may have to divide speed / 2 if moving diagonally
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.direction = direction
        self.width = 4
        self.height = 4
        self.bulletRect = None
        self.speed = 8



    def update(self, event):

        if self.direction == 'up':
            self.y -= self.speed

        elif self.direction == 'down':
            self.y += self.speed

        elif self.direction == 'left':
            self.x -= self.speed

        elif self.direction == 'right':
            self.x += self.speed

        elif self.direction == 'upleft':
            self.x -= (self.speed/2)
            self.y -= (self.speed/2)

        elif self.direction == 'downleft':
            self.x -= (self.speed/2)
            self.y += (self.speed/2)

        elif self.direction == 'upright':
            self.x += (self.speed/2)
            self.y -= (self.speed/2)

        elif self.direction == 'downright':

            self.x += (self.speed/2)
            self.y += (self.speed/2)


        self.bulletRect = pygame.Rect(self.x, self.y, 4, 4)
        pygame.draw.ellipse(DISPLAYSURF, GREEN, (self.bulletRect), 2)





FPS = 30
fpsClock = pygame.time.Clock()


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)



ship = Player(width / 2, height / 2)
bads = Enemy(width / 2, height / 2)



queue = pygame.sprite.Group()
queue.add(ship)
queue.add(bads)


while True:
    DISPLAYSURF.fill(BLACK)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()


                #passes 'event' to everything in the queue and calls
                #their obj.update().  in this way the gameloop
                #is a bit more readable
        for thing in queue:
            thing.update(event)

        try: #i'm not married to this bit of code :/
            checkForShot, shotDirection = ship.shotcheck(event)
            if checkForShot:
                shotx, shoty = ship.playerRect.center
                shot = Bullet(shotx, shoty, shotDirection)
                queue.add(shot)
        except TypeError:
            pass

    pygame.display.flip()
    fpsClock.tick(FPS)