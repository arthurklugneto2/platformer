import copy
import pickle
import json
import os

class SaveSystem:

    def __init__(self):
        self.lastCheckpoint = None
        self.lastCheckpointPlayerPosition = None
        self.lastCheckpointMapName = None   
        self.saveFileName = 'save.json'     

    def saveCheckpoint(self,checkpoint,game):
        if checkpoint.name not in game.activatedCheckpoints:
            game.activatedCheckpoints.append(checkpoint.name)

            self.lastCheckpoint = checkpoint
            self.lastCheckpointPlayerPosition = [game.player.x,game.player.y]
            self.lastCheckpointMapName = game.currentRoom

    def loadCheckpoint(self,game):
        if self.lastCheckpoint != None and self.lastCheckpointPlayerPosition != None and \
            self.lastCheckpointMapName != None:
            game.loadLevel(self.lastCheckpointMapName,game.objects,game.enemies,game.objectsTopLayer,game.objectsWaterLayer,(self.lastCheckpointPlayerPosition[0],self.lastCheckpointPlayerPosition[1]),False)
            game.player.x = self.lastCheckpointPlayerPosition[0]
            game.player.y = self.lastCheckpointPlayerPosition[1]
        else:
            game.loadLevel('1979',game.objects,game.enemies,game.objectsTopLayer,game.objectsWaterLayer,(64,96),False)

    def saveGame(self,checkpoint,game):
        self.saveCheckpoint(checkpoint,game)

        save = {}
        save['levelName'] = game.currentRoom

        save['playerPosition'] = (game.player.x,game.player.y)
        save['playerCoins'] = game.player.coins
        save['playerKeys'] = game.player.keys
        save['playerLife'] = game.player.health
        save['playerMaxLife'] = game.player.maxHealth
        save['playerLives'] = game.player.lives
        save['playerDoubleJump'] = game.player.canDoubleJump

        save['objectsOnce'] = game.objectsOnce
        save['solvedPuzzles'] = game.solvedPuzzles
        save['activationPersist'] = game.activationPersist
        save['activatedCheckpoint'] = game.activatedCheckpoints
        save['switches'] = game.switchSystem.switches

        with open(self.saveFileName, 'w') as outfile:
            json.dump(save, outfile)

    def loadGame(self,game):
        '''
        with open('data.txt') as json_file:
            data = json.load(json_file)
            for p in data['people']:
                print('Name: ' + p['name'])
                print('Website: ' + p['website'])
                print('From: ' + p['from'])
                print('')
        '''
        with open(self.saveFileName) as json_file:
            save = json.load(json_file)
            
            levelName = save['levelName']

            playerX = save['playerPosition'][0]
            playerY = save['playerPosition'][1]
            coins = save['playerCoins']
            keys = save['playerKeys']
            health = save['playerLife']
            maxHealth = save['playerMaxLife']
            lives = save['playerLives']
            doubleJumb = save['playerDoubleJump']

            objectOnce = save['objectsOnce']
            solvedPuzzles = save['solvedPuzzles']
            persists = save['activationPersist']
            activatedCheckpoints = save['activatedCheckpoint']
            switches = save['switches']

            game.loadLevel(levelName,game.objects,game.enemies,game.objectsTopLayer,game.objectsWaterLayer,(playerX,playerY),False)
            
            game.player.coins = coins
            game.player.keys = keys
            game.player.health = health
            game.player.maxHealth = maxHealth
            game.player.lives = lives

            game.objectsOnce = objectOnce
            game.solvedPuzzles = solvedPuzzles
            game.activationPersist = persists
            game.activatedCheckpoints = activatedCheckpoints

            game.switchSystem.switches = switches


    def hasSaveFile(self):
        return os.path.exists(self.saveFileName)