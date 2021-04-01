import pygame
from GameObjects.gameobject import GameObject
from Modules.spriteSheet import SpriteSheet

class Light(GameObject):

    def __init__(self,x,y,w,h,properties,game):

        self.spritePath = './Assets/Objects/light.png'
        
        self.game = game
        self.spriteBaseSize = 16
        self.topoffset = 5
        self.xoffset = 5
        self.setProperties(properties)
        self.x, self.y, self.w, self.h = x, y, 32, 32
        self.startQTBoundaries(self.x,self.y,self.w,self.h)

        self.sprite = SpriteSheet(pygame.image.load(self.spritePath))
        self.off = self.sprite.getimage(0,0,self.spriteBaseSize,self.spriteBaseSize)
        self.on_green = self.sprite.getimage(32,0,self.spriteBaseSize,self.spriteBaseSize)
        self.on_blue = self.sprite.getimage(16,0,self.spriteBaseSize,self.spriteBaseSize)
        self.on_red = self.sprite.getimage(48,0,self.spriteBaseSize,self.spriteBaseSize)

        self.color = None
        if self.have('color'):
            self.color = self.get('color')
            
        self.enabled = True
        if self.have('enabled'):
            self.enabled = bool(self.get('enabled'))

        self.collide = True
        self.collectable = True
        self.isActivated = False
        self.inContactWithPlayer = False

    def draw(self, display,camera):
        if self.isActivated:
            if self.color != None and self.color == 'blue':
                display.blit(pygame.transform.scale(self.on_blue,
                (self.w, self.h)), (self.x+camera.x, self.y+camera.y))
            elif self.color != None and self.color == 'red':
                display.blit(pygame.transform.scale(self.on_red,
                (self.w, self.h)), (self.x+camera.x, self.y+camera.y))
            else:
                display.blit(pygame.transform.scale(self.on_green,
                (self.w, self.h)), (self.x+camera.x, self.y+camera.y))

        else:
            display.blit(pygame.transform.scale(self.off,
                (self.w, self.h)), (self.x+camera.x, self.y+camera.y))

    def update(self, keys):
        pass

    def collisionEvent(self):
        self.inContactWithPlayer = True

    def activationEvent(self):
        pass

    def deactivationEvent(self):
        pass