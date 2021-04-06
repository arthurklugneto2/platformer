from Modules.queue_item import QueueItem
from Modules.lang import Lang

class QueueSystem:

    def __init__(self):
        self.queue = []
        self.defaultMessageTime = 120

    def addItem(self,item):
        self.queue.append(item)

    def update(self, game, uisystem):
        if len(self.queue) > 0:
            item = self.queue[0]
            if item.message != None:
                if not item.isDialog:
                    game.uiSystem.addMessage(item.message,self.defaultMessageTime)
                else:
                    game.uiSystem.addDialog(item.message)
            else:
                if not item.isDialog:
                    game.uiSystem.addMessage(self.getDefaultMessage(item),self.defaultMessageTime)
                else:
                    pass
            self.execute(item,game)
            self.queue.pop(0)

    def execute(self,item,game):
        
        if item.command == 'GIVE_PLAYER':
            params = item.parameters.split(':')
            
            # ===================
            # Collectables
            # ===================
            if params[0] == 'life':
                amount = int(params[1])
                game.player.lives += amount
            if params[0] == 'hearth':
                amount = int(params[1])
                if game.player.maxHealth >= game.player.health + amount:
                    game.player.health += amount
                else:
                    game.player.health = game.player.maxHealth

            # ===================
            # Inventory
            # ===================
            if params[0] == 'pistol':
                game.playerSystem.addItemToInventory('pistol',1)
            

        if item.command == 'PLAYER_SKILL':
            params = item.parameters.split(':')
            if params[0] == 'double_jump' and params[1] == 'True':
                game.player.canDoubleJump = True

    def getDefaultMessage(self,item):
        if item.command == 'GIVE_PLAYER':
            params = item.parameters.split(':')
            if params[0] == 'LIFE':
                amount = int(params[1])
                #return ("You've got "+str(amount)+" UP")
                return Lang.__('player.receive.life',amount)
            if params[0] == 'HEARTH':
                amount = int(params[1])
                #return ("You've got "+str(amount)+" HEARTH")
                return Lang.__('player.receive.hearth',amount)
