import pygame

from pygame.math import Vector2
from Objects.indentoryItem import InventoryItem
from GameObjects.player.pistol_shot import PistolShot

class PlayerSystem:

    def __init__(self,player):
        self.player = player
        self.inventory = []
        self.inventoryIndex = 0
        self.inventoryImage = pygame.image.load('Assets/Player/inventory.png')
        self.inventoryTime = 0
        self.inventoryTimeReset = 15

        self.inventory.append(InventoryItem('pistol',1,self.inventoryImage))
        self.inventory.append(InventoryItem('no_item',0,self.inventoryImage))
        self.inventory.append(InventoryItem('no_item',0,self.inventoryImage))
        self.inventory.append(InventoryItem('no_item',0,self.inventoryImage))
        self.inventory.append(InventoryItem('health_kit',3,self.inventoryImage))

    def update(self,game,keys):
        self.updateInventory(game,keys)

    # ============================
    # Inventory
    # ============================

    def updateInventory(self,game,keys):
        if self.inventoryTime == 0:
            if keys[pygame.K_r]:
                if len(self.inventory) > 0:
                    self.inventoryIndex += 1
                self.inventoryTime = self.inventoryTimeReset
            if keys[pygame.K_t]:
                if len(self.inventory) > 0:
                    self.inventoryIndex -= 1
                self.inventoryTime = self.inventoryTimeReset
            if keys[pygame.K_q]:
                if len(self.inventory) > 0:
                    item = self.inventory[self.inventoryIndex % len(self.inventory)]
                    if item != None and item.canUse(game):
                        item.useItem(game)
                        if item.isRemoveOnUse() and item.quantity <= 1:
                            self.inventory.remove(item)
                        if item.isDisplayQuantity() and item.quantity > 1:
                            item.quantity -= 1
                        self.inventoryTime = self.inventoryTimeReset

        self.inventoryTime -= 1
        if self.inventoryTime < 0: self.inventoryTime = 0

    def addItemToInventory(self,item,quantity):
        self.inventory.append(InventoryItem(item,quantity,self.inventoryImage))

    def removeItemFromInventory(self,item):
        for x in self.inventory:
            if x.name == item:
                self.inventory.remove(x)

    def clearInventory(self):
        self.inventory = []

    def getItensForUi(self):
        if len(self.inventory) > 0:
            for x in range(3):
                prev = self.inventory[(self.inventoryIndex-1) % len(self.inventory)]
                selc = self.inventory[self.inventoryIndex % len(self.inventory)]
                next = self.inventory[(self.inventoryIndex+1) % len(self.inventory)]

            return [prev,selc,next]
        return None

    # ==============================
    # Inventory - Use Itens
    # ==============================
    def useHealthKit(self,game):
        game.audioSystem.playSFX('hearth')
        game.player.health += 1

    def usePistol(self,game):
        game.audioSystem.playSFX('player_hurt')
        mouseX, mouseY = pygame.mouse.get_pos()
        mousePosition = Vector2(mouseX,mouseY)
        cameraPosition = Vector2(game.camera.x,game.camera.y)
        playerPosition = Vector2(game.player.x,game.player.y)
        playerScreen = Vector2((playerPosition.x + cameraPosition.x)*game.uiSystem.scale, (playerPosition.y + cameraPosition.y)*game.uiSystem.scale)
        direction = playerScreen - mousePosition
        direction = direction.normalize() * -8
        angle = pygame.math.Vector2(0,0).angle_to(direction)
        playerShot = PistolShot(playerPosition.x,playerPosition.y,8,8,'',game)
        playerShot.velocity = direction
        playerShot.angle = -angle
        game.objectsWeapon.append(playerShot)