import pygame
from GameObjects.gameobject import GameObject
from Modules.queue_item import QueueItem
from Modules.lang import Lang

class Chest(GameObject):

    def __init__(self,x,y,w,h,properties,game):
        self.openPath = './Assets/Objects/chest_open.png'
        self.closedPath = './Assets/Objects/chest_closed.png'

        self.game = game
        self.spriteBaseSize = 16
        self.topoffset = 0
        self.xoffset = 0
        self.setProperties(properties)

        self.x, self.y, self.w, self.h = x, y, 32, 32
        self.startQTBoundaries(self.x,self.y,self.w,self.h)
        
        self.collide = True
        self.collectable = True
        self.isActivated = False
        self.persistActivation = False
        self.activationDelay = 20
        self.activationDelayMax = 20
        self.inContactWithPlayer = False

        if self.have('persist') : self.persistActivation = True

        self.openImage = pygame.image.load(self.openPath)
        self.closedImage = pygame.image.load(self.closedPath)

    def draw(self, display,camera):
        if self.isActivated:
            display.blit(pygame.transform.scale(self.openImage,
                (self.w, self.h)), (self.x+camera.x, self.y+camera.y))
        else:
            display.blit(pygame.transform.scale(self.closedImage,
                (self.w, self.h)), (self.x+camera.x, self.y+camera.y))

    def update(self, keys):

        if self.persistActivation and [self.game.currentRoom,int(self.x/self.w),int(self.y/self.h)] in self.game.activationPersist:
            self.isActivated = True

        self.activationDelay -= 1
        if self.activationDelay < 0 : self.activationDelay = 0

        if self.inContactWithPlayer and self.activationDelay == 0 and keys[pygame.K_e] and not self.isActivated:
            self.isActivated = True
            self.activationDelay = self.activationDelayMax
            self.activationEvent()
            if self.persistActivation and [self.game.currentRoom,int(self.x/self.w),int(self.y/self.h)] not in self.game.activationPersist:
                self.game.activationPersist.append([self.game.currentRoom,int(self.x/self.w),int(self.y/self.h)])

        self.inContactWithPlayer = False

    def collisionEvent(self):
        self.inContactWithPlayer = True

    def activationEvent(self):
        
        '''
            Give Player
        '''
        self.game.audioSystem.playSFX('boss_dead');
        givePlayers = self.getMany('give_player')
        for givePlayer in givePlayers:
            parts = givePlayer.split('|')
            item = parts[0]
            amount = parts[1]
            message = Lang.__('player.receive',amount,item)
            self.game.queueSystem.addItem( QueueItem('GIVE_PLAYER',parts[0]+':'+parts[1],message) )
        
        '''
            Player Status
        '''
        playerStatusChanges = self.getMany('player')
        for playerStatusChange in playerStatusChanges:
            parts = playerStatusChange.split('|')
            item = parts[0]
            amount = parts[1]
            message = Lang.__('player.skill.double_jump')
            self.game.queueSystem.addItem( QueueItem('PLAYER_SKILL',parts[0]+':'+parts[1],message,True) )

        '''
            Summon Enemy
        '''
        enemySummons = self.getMany('enemy')
        for enemy in enemySummons:
            self.game.addEnemy(enemy)
