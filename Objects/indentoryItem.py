import pygame
from Modules.spriteSheet import SpriteSheet
from GameObjects.player.pistol_shot import PistolShot

class InventoryItem:

    def __init__(self,name,quantity,image):
        self.name = name
        self.quantity = quantity
        self.spriteSize = 16
        self.imageFile = image
        self.image = SpriteSheet(image)

    def getDrawable(self):
        if self.name == 'no_item':
            return self.image.getimage(0,0,self.spriteSize,self.spriteSize)
        if self.name == 'health_kit':
            return self.image.getimage(16,0,self.spriteSize,self.spriteSize)
        if self.name == 'red_key':
            return self.image.getimage(32,0,self.spriteSize,self.spriteSize)
        if self.name == 'blue_key':
            return self.image.getimage(48,0,self.spriteSize,self.spriteSize)
        if self.name == 'green_key':
            return self.image.getimage(64,0,self.spriteSize,self.spriteSize)
        if self.name == 'pistol':
            return self.image.getimage(80,0,self.spriteSize,self.spriteSize)

    def isDisplayQuantity(self):
        if self.name == 'no_item':
            return False
        if self.name == 'health_kit':
            return True
        if self.name == 'red_key':
            return False
        if self.name == 'blue_key':
            return False
        if self.name == 'green_key':
            return False
        if self.name == 'pistol':
            return False

    def isRemoveOnUse(self):
        if self.name == 'no_item':
            return False
        if self.name == 'health_kit':
            return True
        if self.name == 'red_key':
            return False
        if self.name == 'blue_key':
            return False
        if self.name == 'green_key':
            return False
        if self.name == 'pistol':
            return False
    
    def canUse(self,game):
        if self.name == 'health_kit' and game.player.health < game.player.maxHealth:
            return True
        if self.name == 'pistol':
            return True
        return False

    def useItem(self,game):
        if self.name != 'no_item':
            if self.name == 'health_kit':
                game.playerSystem.useHealthKit(game)
            if self.name == 'pistol':
                game.playerSystem.usePistol(game)
                
