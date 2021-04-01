import pygame
from Modules.spriteSheet import SpriteSheet
from Modules.spriteAnimation import SpriteAnimation

class Effect(object):

    def __init__(self,x,y,w,h,path,loop,frameQuantity,frameSpeed):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.life = frameQuantity*frameSpeed
        self.loop = loop
        self.frameQuantity = frameQuantity
        self.frameSpeed = frameSpeed

        self.sprite = SpriteSheet(pygame.image.load(path))
        self.animation = SpriteAnimation(frameQuantity,frameSpeed,loop)
        self.effect = [self.sprite.getimage(x * self.w,0,self.w,self.h) for x in range(frameQuantity)]

    def update(self,effectSystem):
        self.animation.update()
        if not self.loop:
            self.life -= 1
            if self.life <= 0:
                effectSystem.effects.remove(self)

    def draw(self,display,camera):
        #self.effect[self.animation.get()]
        display.blit( pygame.transform.scale( self.effect[self.animation.get()],(self.w*2,self.h*2) )
            ,(self.x+camera.x, self.y + camera.y))