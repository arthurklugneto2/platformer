import pygame
from Objects.enemy import Enemy
from Modules.spriteSheet import SpriteSheet

class Spike(Enemy):

    def __init__(self,x,y,w,h,props,game):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.cs = (-8,-12)
        self.co = (4,12)
        self.spritePath = './Assets/Enemies/spike.png'
        self.props= props
        self.game = game
        self.spriteBaseSize = 16
        self.hurtAmount = 1

        self.sprite = SpriteSheet(pygame.image.load(self.spritePath))
        self.spike = self.sprite.getimage(0,0,self.spriteBaseSize,self.spriteBaseSize)
        if props != None:
            if props == 'T':
                self.spike = self.sprite.getimage(16,0,self.spriteBaseSize,self.spriteBaseSize)
            elif props == 'L':
                self.spike = self.sprite.getimage(32,0,self.spriteBaseSize,self.spriteBaseSize)
            elif props == 'R':
                self.spike = self.sprite.getimage(48,0,self.spriteBaseSize,self.spriteBaseSize)

    def draw(self, display,camera):
        display.blit(pygame.transform.scale(self.spike,
                (self.w,self.h)), (self.x+camera.x, self.y + camera.y))
    
    def update(self, keys):
        pass

    def hurt(self):
        pass