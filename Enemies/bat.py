import pygame
from pygame.math import Vector2
from Objects.enemy import Enemy
from Modules.spriteSheet import SpriteSheet
from Modules.spriteAnimation import SpriteAnimation

class Bat(Enemy):

    def __init__(self,x,y,w,h,props,game):
        Enemy.__init__(self,x,y,w,h,props,game)
        self.x, self.y, self.w, self.h = x, y, w, h
        self.setProperties(props)
        self.spritePathPrefix = './Assets/Enemies/'
        self.game = game
        self.spriteBaseSize = 16
        self.hurtAmount = 1
        self.cs = (0,0)
        self.co = (0,0)
        self.activationDistance = 250
        self.originalPosition = Vector2(self.x,self.y)
        self.interpolatorCount = 0
        self.hurtCount = 60
        self.maxHurtCount = 60
        self.state = 'IDLE'
        self.drop = None
        self.dropAdded = False

        self.setupSprite()
                
    def setupSprite(self):
        # IDLE
        self.idleSprite = SpriteSheet(pygame.image.load(self.spritePathPrefix+'bat_idle.png'))
        self.idleAnimation = SpriteAnimation(4,30,True)
        self.idleState = [self.idleSprite.getimage(self.spriteBaseSize * x, 0, 
                        self.spriteBaseSize, self.spriteBaseSize) for x in range(self.idleAnimation.framesQuantity)]
        self.game.animationSystem.addAnimation(self.idleAnimation)

        # WALK
        self.walkSprite = SpriteSheet(pygame.image.load(self.spritePathPrefix+'bat_walk.png'))
        self.walkAnimation = SpriteAnimation(4,10,True)
        self.walkState = [self.walkSprite.getimage(self.spriteBaseSize * x, 0, 
                        self.spriteBaseSize, self.spriteBaseSize) for x in range(self.walkAnimation.framesQuantity)]
        self.game.animationSystem.addAnimation(self.walkAnimation)

    def draw(self, display,camera):
        if self.velocity.length() != 0.0:
            display.blit(pygame.transform.scale(self.walkState[self.walkAnimation.get()],
                        (self.w,self.h)), (self.position.x+camera.x, self.position.y + camera.y))
        else:
            display.blit(pygame.transform.scale(self.idleState[self.idleAnimation.get()],
                        (self.w,self.h)), (self.position.x+camera.x, self.position.y + camera.y))

    def update(self, keys):

        playerPosition = Vector2(self.game.player.x,self.game.player.y)
        enemyPosition = Vector2(self.position.x, self.position.y)

        direction = playerPosition-enemyPosition
        distance = direction.length()
        if distance < self.activationDistance :
            self.acceleration = direction
            self.interpolatorCount = 0
            self.state = 'ATTACK'
        else:
            self.state = 'IDLE'
            self.interpolatorCount += 0.01
            if self.interpolatorCount > 1: self.interpolatorCount = 1
            self.velocity.x = 0
            self.velocity.y = 0
            currentPosition = Vector2(self.x,self.y)
            toHome = currentPosition.lerp(self.originalPosition,self.interpolatorCount)
            self.position = toHome

        Enemy.update(self,keys)
        self.x = self.position.x
        self.y = self.position.y
        self.hurtCount -= 1
        if self.hurtCount < 0 : self.hurtCount = 0

    def hurt(self):
        if self.hurtCount == 0:
            self.state = 'KILL'
            self.game.audioSystem.playSFX('bat_dead');
            self.hurtCount = self.maxHurtCount
            self.game.effectsSystem.generateEffect('BAT_KILL',self.x,self.y-20,0,16)
            self.game.enemies.remove(self)
            if self.drop != None and not self.dropAdded:
                self.game.queueSystem.addItem(self.drop)
                self.dropAdded = True
            elif self.drop == None and not self.dropAdded:
                drop = self.game.enemySystem.enemyDefaultDrop(self)
                if drop != None:
                    self.game.queueSystem.addItem(drop)
                self.dropAdded = True