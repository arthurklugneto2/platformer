import pygame
from Modules.spriteSheet import SpriteSheet
from Modules.spriteAnimation import SpriteAnimation
from GameObjects.gameobject import GameObject

class Computer(GameObject):

    def __init__(self,x,y,w,h,properties,game):
        
        self.spritePath = './Assets/Objects/computer.png'
        self.game = game
        self.spriteBaseSize = 16
        self.topoffset = 5
        self.xoffset = 0
        self.setProperties(properties)

        self.x, self.y, self.w, self.h = x, y, 32, 32
        self.startQTBoundaries(self.x,self.y,self.w,self.h)
        
        self.collide = True
        self.collectable = True
        self.collected = False
        self.collisionExecuted = False
        self.inContactWithPlayer = False
        self.activationDelay = 20
        self.activationDelayMax = 20

        self.idleSprite = SpriteSheet(pygame.image.load(self.spritePath))
        self.idleAnimation = SpriteAnimation(4,30,True)
        self.idleState = [self.idleSprite.getimage(32 * x, 0, 32, self.spriteBaseSize) for x in range(self.idleAnimation.framesQuantity)]
        self.game.animationSystem.addAnimation(self.idleAnimation)

    def draw(self, display,camera):
        display.blit(pygame.transform.scale(self.idleState[self.idleAnimation.get()],
                (64, self.h)), (self.x+camera.x, self.y + camera.y))

    def update(self, keys):
        self.activationDelay -= 1
        if self.activationDelay < 0 : self.activationDelay = 0

        if self.inContactWithPlayer and self.activationDelay == 0 and keys[pygame.K_e]:
            self.isActivated = True
            self.activationDelay = self.activationDelayMax
            self.activationEvent()

        self.inContactWithPlayer = False

    def collisionEvent(self):
        self.inContactWithPlayer = True

    def activationEvent(self):
        if self.properties != None:
            self.game.audioSystem.playSFX('computer');
            # process dialogs
            dialogs = self.getMany('dialog')
            if len(dialogs) > 0:
                for x in range( len(dialogs) ):
                    self.game.uiSystem.addDialog(dialogs[x])