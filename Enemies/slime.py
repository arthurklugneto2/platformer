import pygame
import math
from Objects.enemy import Enemy
from Modules.spriteSheet import SpriteSheet
from Modules.spriteAnimation import SpriteAnimation
from Modules.mathFunctions import MathFunctions
from Modules.queue_item import QueueItem

class Slime(Enemy):

    def __init__(self,x,y,w,h,props,game):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.cs = (-8,-12)
        self.co = (4,12)
        self.killAnimationTime = 30
        self.spritePathPrefix = './Assets/Enemies/'
        self.setProperties(props)
        self.game = game
        self.spriteBaseSize = 16
        self.hurtAmount = 1
        self.mathUtil = MathFunctions()

        self.velX = 0
        self.velY = 0

        self.state = "NORMAL"
        self.movSpeed = 0.003

        self.startXPosition = self.x / 32
        self.startYPosition = self.y / 32
        self.endXPosition = self.x / 32
        self.endYPosition = self.y / 32
        if self.have('x'):
            self.endXPosition = int(self.get('x'))
        if self.have('y'):
            self.endYPosition = int(self.get('y'))

        self.movement = [self.startXPosition, self.startYPosition, self.endXPosition, self.endYPosition]
        self.movementTimer = 0
        self.drop = None
        self.dropAdded = False
        
        if self.have('drop'):
            attr = self.get('drop').split('|')
            self.drop = QueueItem(attr[0],attr[1]+':'+attr[2])

        # Idle State
        self.idleSprite = SpriteSheet(pygame.image.load(self.spritePathPrefix+'slime_idle.png'))
        self.idleAnimation = SpriteAnimation(5,10,True)
        self.idleState = [self.idleSprite.getimage(self.spriteBaseSize * x, 0, 
                        self.spriteBaseSize, self.spriteBaseSize) for x in range(self.idleAnimation.framesQuantity)]
        self.game.animationSystem.addAnimation(self.idleAnimation)

        # Walk State
        self.walkSprite = SpriteSheet(pygame.image.load(self.spritePathPrefix+'slime_walk.png'))
        self.walkAnimation = SpriteAnimation(2,20,True)
        self.walkState = [self.walkSprite.getimage(self.spriteBaseSize * x, 0, 
                        self.spriteBaseSize, self.spriteBaseSize) for x in range(self.walkAnimation.framesQuantity)]
        self.game.animationSystem.addAnimation(self.walkAnimation)

        # Kill State
        self.killSprite = SpriteSheet(pygame.image.load(self.spritePathPrefix+'slime_kill.png'))
        self.killState = [self.killSprite.getimage(0, 0, self.spriteBaseSize, self.spriteBaseSize)]

    def draw(self, display,camera):
        if self.state != 'KILL':
            if self.velX == 0 and self.velY == 0:
                display.blit(pygame.transform.scale(self.idleState[self.idleAnimation.get()],
                    (self.w,self.h)), (self.x+camera.x, self.y + camera.y))
            elif self.velX < 0:
                if self.state != 'ATTACK':
                    display.blit(pygame.transform.scale(self.walkState[self.walkAnimation.get()],
                            (self.w,self.h)), (self.x+camera.x, self.y + camera.y))
                else:
                    display.blit(pygame.transform.scale(self.attackState[self.attackAnimation.get()],
                            (self.w,self.h)), (self.x+camera.x, self.y + camera.y))
            elif self.velX > 0:
                if self.state != 'ATTACK':
                    display.blit( pygame.transform.flip(pygame.transform.scale(self.walkState[self.walkAnimation.get()],
                            (self.w,self.h)), 1, 0) , (self.x+camera.x, self.y + camera.y))
                else:
                    display.blit( pygame.transform.flip(pygame.transform.scale(self.attackState[self.attackAnimation.get()],
                            (self.w,self.h)), 1, 0) , (self.x+camera.x, self.y + camera.y))

        else:
            display.blit(pygame.transform.scale(self.killState[0],
                    (self.w, self.h)), (self.x+camera.x, self.y+camera.y))

    def update(self, keys):
        calcX = self.x
        calcY = self.y

        if self.state != 'KILL' and self.movement != None:
            mov = self.movement
            xPos = self.mathUtil.sawTooth(mov[0]*self.w,mov[2]*self.w,self.movementTimer)
            self.movementTimer += self.movSpeed
            if self.movementTimer > 1: self.movementTimer = 0
            self.x = xPos

        if self.state == 'KILL' and self.killAnimationTime > 0:
            self.killAnimationTime -= 1
        if self.killAnimationTime <= 0:
            self.game.enemies.remove(self)      

        self.velX = self.x - calcX
        self.velY = self.y - calcY

    def hurt(self):
        self.state = 'KILL'
        self.game.audioSystem.playSFX('slime_dead');
        self.game.effectsSystem.generateEffect('COLLECTED',self.x,self.y,0,16)
        if self.drop != None and not self.dropAdded:
            self.game.queueSystem.addItem(self.drop)
            self.dropAdded = True
        elif self.drop == None and not self.dropAdded:
            drop = self.game.enemySystem.enemyDefaultDrop(self)
            if drop != None:
                self.game.queueSystem.addItem(drop)
            self.dropAdded = True