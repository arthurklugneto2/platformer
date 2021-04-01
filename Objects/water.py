import pygame
from Objects.quadTreeItem import QuadTreeItem

class Water(QuadTreeItem):
    def __init__(self, x, y, w, h, image):
        self.x, self.y, self.w, self.h, self.image = x, y, w, h, image
        self.startQTBoundaries(self.x,self.y,self.w,self.h)
        self.collide = True
        self.collectable = True

        self.topoffset = 0
        self.xoffset = 0

    def draw(self, display,camera):
        #screen.blit(image,(100,100),area = None,special_flags=py.BLEND_RGBA_ADD(blending))
        display.blit(self.image, (self.x+camera.x, self.y+camera.y),area=None,special_flags=pygame.BLEND_RGB_MULT)

    def update(self, keys):
        pass

    def collisionEvent(self):
        pass
