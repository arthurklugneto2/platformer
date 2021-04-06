import pygame
from Modules.spriteSheet import SpriteSheet
from GameObjects.gameobject import GameObject
from GameObjects.player.player_shot import PlayerShot
from pygame.math import Vector2

class PistolShot(PlayerShot):

    def __init__(self,x,y,w,h,props,game):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.setProperties(props)
        self.imagePath = './Assets/Player/pistol_shot.png'
        self.game = game
        self.spriteBaseSize = 8
        self.hurtAmount = 1
        self.velocity = Vector2(0,0)
        self.angle = 0
        self.life = 60

        self.sprite = SpriteSheet(pygame.image.load(self.imagePath))
        self.bullet = self.sprite.getimage(0,0,self.spriteBaseSize,self.spriteBaseSize)

    def update(self):

        self.x += self.velocity.x
        self.y += self.velocity.y

        self.life -= 1

    def draw(self,display,camera):
        display.blit(pygame.transform.rotate(pygame.transform.scale(self.bullet,
                (self.w*2, self.h*2)),self.angle), (self.x+camera.x, self.y+camera.y))