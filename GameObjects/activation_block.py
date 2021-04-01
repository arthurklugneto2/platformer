import pygame
from GameObjects.gameobject import GameObject

class ActivationBlock(GameObject):

    def __init__(self,x,y,w,h,properties,game):
        self.spritePath = './Assets/Objects/activation_block.png'

        self.game = game
        self.spriteBaseSize = 16
        self.topoffset = 18
        self.xoffset = 19
        self.setProperties(properties)

        self.x, self.y, self.w, self.h = x, y, 32, 32
        self.startQTBoundaries(self.x,self.y,self.w,self.h)
        
        self.collide = True
        self.collectable = False
        self.collisionExecuted = False
        self.activationSwitch = None
        self.activationPuzzle = None
        if self.have('switch'):
            self.activationSwitch = self.get('switch')
        if self.have('puzzle'):
            self.activationPuzzle = self.get('puzzle')

        self.image = pygame.image.load(self.spritePath)

    def draw(self, display,camera):
        display.blit(pygame.transform.scale(self.image,
                (self.w, self.h)), (self.x+camera.x, self.y+camera.y))

    def update(self, keys):
        if self.activationSwitch != None:
            if self.game.switchSystem.hasSwitch(self.activationSwitch):
                self.game.removeQuadTreeItem(self)
                self.game.objects.remove(self)
        if self.activationPuzzle != None:
            if self.activationPuzzle in self.game.solvedPuzzles:
                self.game.removeQuadTreeItem(self)
                self.game.objects.remove(self)

    def collisionEvent(self):
        self.game.audioSystem.playSFX('slime_dead');