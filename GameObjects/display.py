import pygame
from Modules.spriteSheet import SpriteSheet
from GameObjects.gameobject import GameObject

class Display(GameObject):

    def __init__(self,x,y,w,h,properties,game):
        self.spritePath = './Assets/Objects/display.png'

        self.game = game
        self.topoffset = 5
        self.xoffset = 5
        self.setProperties(properties)
        self.x, self.y,self.w,self.h = x, y, w, h
        self.startQTBoundaries(self.x,self.y,self.w,self.h)
        self.sprite = SpriteSheet(pygame.image.load(self.spritePath))
        
        self.value = ''
        self.prefix = ''
        self.sufix = ''
        self.size = 2

        if self.have('size') : self.size = int(self.get('size'))
        if self.have('value') : self.value = self.get('value')
        if self.have('prefix') : self.prefix = self.get('prefix')
        if self.have('sufix') : self.sufix = self.get('sufix')

        self.collide = False
        self.collectable = True
        self.activationDelay = 20
        self.activationDelayMax = 20

        self.display_single = self.sprite.getimage(0,0,16,16)
        self.display_double = self.sprite.getimage(16,0,32,16)
        self.display_triple = self.sprite.getimage(48,0,48,16)

    def draw(self, display,camera):
        if self.size == 1:
            display.blit(pygame.transform.scale(self.display_single,
                (32, 32)), (self.x+camera.x, self.y+camera.y))
        elif self.size == 2:
            display.blit(pygame.transform.scale(self.display_double,
                (64, 32)), (self.x+camera.x, self.y+camera.y))
        elif self.size == 3:
            display.blit(pygame.transform.scale(self.display_triple,
                (128, 32)), (self.x+camera.x, self.y+camera.y))

        xOff = 0
        if self.size == 1: xOff = 16
        if self.size == 2: xOff = 32
        if self.size == 3: xOff = 64

        # value
        valueSurface2 = self.game.uiSystem.displayFont.render(str(self.prefix)+str(self.value)+str(self.sufix),True,(50,50,50))
        display.blit(valueSurface2,(self.x+camera.x+xOff-(valueSurface2.get_width()/2)+1,self.y+camera.y+5+1))

    def update(self, keys):
        pass

