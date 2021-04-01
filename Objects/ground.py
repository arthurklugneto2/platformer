import pygame
from Objects.quadTreeItem import QuadTreeItem

class Ground(QuadTreeItem):
    def __init__(self, x, y, w, h, image):
        self.x, self.y, self.w, self.h, self.image = x, y, w, h, image
        self.startQTBoundaries(self.x,self.y,self.w,self.h)
        self.collide = True
        self.collectable = False

        self.topoffset = 0
        self.xoffset = 0

    def draw(self, display,camera):
        display.blit(self.image, (self.x+camera.x, self.y+camera.y))

    def update(self, keys):
        pass
