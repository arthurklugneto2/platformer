import pygame

class AnimationSystem:

    def __init__(self):
        self.animations = []

    def addAnimation(self, spriteAnimation):
        self.animations.append(spriteAnimation)

    def update(self):
        for animation in self.animations:
            animation.update()