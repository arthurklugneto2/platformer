import pygame
from Modules.spriteSheet import SpriteSheet
from Modules.spriteAnimation import SpriteAnimation
from GameObjects.gameobject import GameObject

class WaterSurface(GameObject):

    def __init__(self,x,y,w,h,properties,game):
        self.x, self.y, self.w, self.h = x, y, 32, 32
        self.startQTBoundaries(self.x,self.y,self.w,self.h)
        self.setProperties(properties)

        self.spritePath = './Assets/Objects/water_surface_blue.png'
        self.spritePathBorder = './Assets/Objects/water_surface.png'
        if self.have('color'):
            color = self.get('color')
            self.spritePath = self.spritePath.replace('blue',color)

        self.game = game
        self.spriteBaseSize = 16
        self.topoffset = 5
        self.xoffset = 5

        self.collide = True
        self.collectable = True
        self.collisionExecuted = False

        # IDLE Graphics
        self.idleSprite = SpriteSheet(pygame.image.load(self.spritePath))
        self.idleAnimation = SpriteAnimation(8,10,True)
        self.idleState = [self.idleSprite.getimage(self.spriteBaseSize * x, 0, self.spriteBaseSize, self.spriteBaseSize) for x in range(self.idleAnimation.framesQuantity)]
        self.game.animationSystem.addAnimation(self.idleAnimation)

        self.idleSpriteBorder = SpriteSheet(pygame.image.load(self.spritePathBorder))
        self.idleAnimationBorder = SpriteAnimation(8,10,True)
        self.idleStateBorder = [self.idleSpriteBorder.getimage(self.spriteBaseSize * x, 0, self.spriteBaseSize, self.spriteBaseSize) for x in range(self.idleAnimationBorder.framesQuantity)]
        self.game.animationSystem.addAnimation(self.idleAnimationBorder)



    def draw(self, display,camera):
        display.blit(pygame.transform.scale(self.idleStateBorder[self.idleAnimationBorder.get()],
            (self.w, self.h)), (self.x+camera.x, self.y + camera.y))
        display.blit(pygame.transform.scale(self.idleState[self.idleAnimation.get()],
            (self.w, self.h)), (self.x+camera.x, self.y + camera.y),area=None,special_flags=pygame.BLEND_RGB_MULT)

    def update(self, keys):
        pass

    def collisionEvent(self):
        if not self.collisionExecuted:
            self.collisionExecuted = True
