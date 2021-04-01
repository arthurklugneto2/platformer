import pygame
from Modules.spriteSheet import SpriteSheet
from Modules.spriteAnimation import SpriteAnimation
from GameObjects.gameobject import GameObject

class Hearth(GameObject):

    def __init__(self,x,y,w,h,properties,game):
        
        self.spritePath = './Assets/Objects/hearth.png'
        self.game = game
        self.spriteBaseSize = 16
        self.topoffset = 5
        self.xoffset = 5
        self.setProperties(properties)
        
        self.x, self.y, self.w, self.h = x, y, 32, 32
        self.startQTBoundaries(self.x,self.y,self.w,self.h)
        
        self.collide = True
        self.collectable = True
        self.collected = False
        self.collisionExecuted = False

        # IDLE Graphics
        self.idleSprite = SpriteSheet(pygame.image.load(self.spritePath))
        self.idleAnimation = SpriteAnimation(4,10,True)
        self.idleState = [self.idleSprite.getimage(self.spriteBaseSize * x, 0, self.spriteBaseSize, self.spriteBaseSize) for x in range(self.idleAnimation.framesQuantity)]
        self.game.animationSystem.addAnimation(self.idleAnimation)

    def draw(self, display,camera):
        display.blit(pygame.transform.scale(self.idleState[self.idleAnimation.get()],
                                                         (self.w, self.h)), (self.x+camera.x, self.y+camera.y))

    def update(self, keys):
        pass

    def collisionEvent(self):
        if not self.collisionExecuted:
            self.game.player.health += 1
            if self.get('once'):
                self.game.objectsOnce.append([self.game.currentRoom,int(self.x/self.w),int(self.y/self.h)])
            if self.game.player.health > self.game.player.maxHealth:
                self.game.player.health = self.game.player.maxHealth
            self.game.objects.remove(self)
            self.game.removeQuadTreeItem(self)
            self.game.effectsSystem.generateEffect('COLLECTED',self.x,self.y)
            self.game.audioSystem.playSFX('hearth');
            self.collisionExecuted = True