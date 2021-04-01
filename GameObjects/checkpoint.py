import pygame
from Modules.spriteSheet import SpriteSheet
from GameObjects.gameobject import GameObject

class Checkpoint(GameObject):

    def __init__(self,x,y,w,h,properties,game):

        self.spritePath = './Assets/Objects/checkpoint.png'
        
        self.game = game
        self.spriteBaseSize = 16
        self.topoffset = 5
        self.xoffset = 5
        self.setProperties(properties)
        self.x, self.y, self.w, self.h = x, y, 32, 32
        self.startQTBoundaries(self.x,self.y,self.w,self.h)

        self.sprite = SpriteSheet(pygame.image.load(self.spritePath))
        self.off = self.sprite.getimage(0,0,self.spriteBaseSize,self.spriteBaseSize)
        self.on = self.sprite.getimage(16,0,self.spriteBaseSize,self.spriteBaseSize)

        self.name = None
        if self.have('name'):
            self.name = self.get('name')
            
        self.collide = True
        self.collectable = True
        self.isActivated = False
        self.actionExecuted = False
        self.inContactWithPlayer = False

    def draw(self, display,camera):
        if self.isActivated:
            display.blit(pygame.transform.scale(self.on,
                (self.w, self.h)), (self.x+camera.x, self.y+camera.y))
        else:
            display.blit(pygame.transform.scale(self.off,
                (self.w, self.h)), (self.x+camera.x, self.y+camera.y))

    def update(self, keys):
        if self.name != None:
            if self.name in self.game.activatedCheckpoints:
                self.actionExecuted = True
                self.isActivated = True

    def collisionEvent(self):
        self.inContactWithPlayer = True
        if not self.actionExecuted:
            self.actionExecuted = True
            self.game.audioSystem.playSFX('computer');
            self.activationEvent()

    def activationEvent(self):
        self.isActivated = True
        self.game.saveSystem.saveCheckpoint(self,self.game)

    def deactivationEvent(self):
        pass
