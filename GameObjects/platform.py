import pygame
import math

class Platform(object):

    def __init__(self,x,y,w,h,properties,game):

        self.spritePath = './Assets/Objects/platform.png'
        self.game = game
        self.spriteBaseSize = 16
        self.topoffset = 0
        self.xoffset = 0
        self.x, self.y, self.w, self.h = x, y, w, h
        self.startQTBoundaries(self.x,self.y,self.w,self.h)
        self.collide = True
        self.collectable = False
        self.angle = 0
        self.platformOffset = [0,0]

        self.image = pygame.image.load(self.spritePath)

    def draw(self, display,camera):
        display.blit(pygame.transform.scale(self.image,(32,32)), (self.x+camera.x, self.y + camera.y))

    def update(self, keys):
        offSetY = math.cos(self.angle)*1
        self.y += (offSetY)
        self.platformOffset[1] = offSetY
        # self.x += (math.cos(self.angle)*0.5)
        self.angle += 0.01

    def collisionEvent(self):
        pass

