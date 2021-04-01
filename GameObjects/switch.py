import pygame
from GameObjects.gameobject import GameObject

class Switch(GameObject):

    def __init__(self,x,y,w,h,properties,game):
        self.onPath = './Assets/Objects/switch_on.png'
        self.offPath = './Assets/Objects/switch_off.png'

        self.game = game
        self.spriteBaseSize = 16
        self.topoffset = 5
        self.xoffset = 5
        self.setProperties(properties)
        self.xAct = None
        if self.have('x'):
            self.xAct = self.get('x')
        self.yAct = None
        if self.have('y'):
            self.yAct = self.get('y')

        self.x, self.y, self.w, self.h = x, y, 32, 32
        self.startQTBoundaries(self.x,self.y,self.w,self.h)
        
        self.collide = True
        self.collectable = True
        self.isActivated = False
        self.activationDelay = 20
        self.activationDelayMax = 20
        self.inContactWithPlayer = False

        self.onImage = pygame.image.load(self.onPath)
        self.offImage = pygame.image.load(self.offPath)

    def draw(self, display,camera):
        if self.isActivated:
            display.blit(pygame.transform.scale(self.onImage,
                (self.w, self.h)), (self.x+camera.x, self.y+camera.y))
        else:
            display.blit(pygame.transform.scale(self.offImage,
                (self.w, self.h)), (self.x+camera.x, self.y+camera.y))

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
        if self.xAct != None and self.yAct != None:
            obj = self.game.getObjectAt(int(self.xAct)*32,int(self.yAct)*32)
            if obj != None:
                self.game.objects.remove(obj)
                self.game.removeQuadTreeItem(obj)