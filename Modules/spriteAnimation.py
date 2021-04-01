import pygame

class SpriteAnimation:

    def __init__(self,length,delay,loop):
        self.delay = delay
        self.currDelay = 0
        self.currentFrame = 0

        self.framesQuantity = length
        self.isLoop = loop
        self.isEnabled = True
        self.removeOnComplete = True

    def get(self):
        return self.currentFrame % self.framesQuantity

    def update(self):
        if self.isEnabled:
            if self.currDelay == self.delay:
                self.currentFrame += 1
                self.currDelay = 0
            else:
                self.currDelay += 1

    def isFinished(self):
        return self.currentFrame == self.framesQuantity