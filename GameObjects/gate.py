import pygame
from Modules.spriteSheet import SpriteSheet
from Modules.spriteAnimation import SpriteAnimation
from GameObjects.gameobject import GameObject

class Gate(GameObject):

    def __init__(self,x,y,w,h,properties,game):
        
        self.spritePath = './Assets/Objects/gate.png'
        self.setProperties(properties)

        self.game = game
        self.spriteBaseSize = 16
        self.topoffset = 5
        self.xoffset = 5

        self.x, self.y, self.w, self.h = x, y, 32, 32
        self.startQTBoundaries(self.x,self.y,self.w,self.h)
        
        self.collide = True
        self.collectable = False
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
        if not self.collisionExecuted:
            if self.get('once'):
                self.game.objectsOnce.append([self.game.currentRoom,int(self.x/self.w),int(self.y/self.h)])
            self.collisionExecuted = True
            self.game.audioSystem.playSFX('slime_dead');