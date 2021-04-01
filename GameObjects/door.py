import pygame
from Modules.spriteSheet import SpriteSheet
from Modules.spriteAnimation import SpriteAnimation
from GameObjects.gameobject import GameObject

class Door(GameObject):

    def __init__(self,x,y,w,h,properties,game):

        self.spritePathOpen = './Assets/Objects/door_open.png'
        self.spritePathClosed = './Assets/Objects/door_close.png'
        self.spritePathOpenCoin = './Assets/Objects/door_open_coin.png'
        self.spritePathClosedCoin = './Assets/Objects/door_close_coin.png'
        self.spritePathOpenEnemy = './Assets/Objects/door_open_enemies.png'
        self.spritePathClosedEnemy = './Assets/Objects/door_close_enemies.png'

        self.game = game
        self.spriteBaseSize = 16
        self.topoffset = 18
        self.xoffset = 19
        self.setProperties(properties)

        self.enemyDoor = self.have('enemy')
        self.coinDoor = self.have('coin')       

        self.x, self.y, self.w, self.h = x, y, 32, 32
        self.startQTBoundaries(self.x,self.y,self.w,self.h)

        self.collide = True
        self.collectable = True
        self.collected = False
        self.collisionExecuted = False
        self.opened = True

        if self.enemyDoor:
            self.openSprite = SpriteSheet(pygame.image.load(self.spritePathOpenEnemy))
            self.closeSprite = SpriteSheet(pygame.image.load(self.spritePathClosedEnemy))
        elif self.coinDoor:
            self.openSprite = SpriteSheet(pygame.image.load(self.spritePathOpenCoin))
            self.closeSprite = SpriteSheet(pygame.image.load(self.spritePathClosedCoin))
        else:
            self.openSprite = SpriteSheet(pygame.image.load(self.spritePathOpen))
            self.closeSprite = SpriteSheet(pygame.image.load(self.spritePathClosed))

        self.openAnimation = SpriteAnimation(10,5,False)
        self.openState = [self.openSprite.getimage(self.spriteBaseSize * x, 0, self.spriteBaseSize, self.spriteBaseSize) for x in range(self.openAnimation.framesQuantity)]
        self.game.animationSystem.addAnimation(self.openAnimation)

    def draw(self,display,camera):
        if self.opened:
            display.blit(pygame.transform.scale(self.openState[self.openAnimation.get()],
                                                         (self.w, self.h)), (self.x+camera.x, self.y+camera.y))
        else:
            display.blit(pygame.transform.scale(self.closeSprite.getimage(0, 0, self.spriteBaseSize, 
            self.spriteBaseSize),(self.w, self.h)), (self.x+camera.x, self.y+camera.y))

    def update(self,keys):
        if self.coinDoor:
            if self.game.countCoins() != 0:
                self.opened = False
            else:
                self.opened = True
        elif self.enemyDoor:
            if self.game.countEnemies() != 0:
                self.opened = False
            else:
                self.opened = True
        else:
            self.opened = True

    def collisionEvent(self):
        if self.opened:
            if self.properties != None:
                map = self.get('map')
                x = self.get('x')
                y = self.get('y')
                self.game.audioSystem.playSFX('boss_dead');
                self.game.loadLevel(map,self.game.objects,self.game.enemies,self.game.objectsTopLayer,self.game.objectsWaterLayer,(int(x)*32,int(y)*32),False)