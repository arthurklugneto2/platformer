import pygame
from Modules.spriteSheet import SpriteSheet
from Modules.spriteAnimation import SpriteAnimation
from GameObjects.gameobject import GameObject

class Vine(GameObject):

    def __init__(self,x,y,w,h,properties,game):
        
        self.spritePath = './Assets/Objects/vine.png'
        self.game = game
        self.setProperties(properties)
        self.spriteBaseSize = 16
        self.topoffset = 18
        self.xoffset = 19

        self.x, self.y, self.w, self.h = x, y, 32, 32
        self.startQTBoundaries(self.x,self.y,self.w,self.h)
        
        self.collide = True
        self.collectable = True
        self.collected = False
        self.collisionExecuted = False

        # IDLE Graphics
        self.idleSprite = SpriteSheet(pygame.image.load(self.spritePath))
        self.idleState = [self.idleSprite.getimage(0, 0, self.spriteBaseSize, self.spriteBaseSize)]

    def draw(self, display,camera):
        display.blit(pygame.transform.scale(self.idleState[0],
                    (self.w, self.h)), (self.x+camera.x, self.y+camera.y))

    def update(self, keys):
        pass

    def collisionEvent(self):
        self.game.player.isOnVine = True