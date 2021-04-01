import copy
import pickle

class SaveSystem:

    ## What has to be saved A COPY of

    def __init__(self):
        self.lastCheckpoint = None
        self.lastCheckpointPlayerPosition = None
        self.lastCheckpointMapName = None        

        # self.playerPosition = [0,0]
        # self.level = ''

    def saveCheckpoint(self,checkpoint,game):
        if checkpoint.name not in game.activatedCheckpoints:
            game.activatedCheckpoints.append(checkpoint.name)

            self.lastCheckpoint = checkpoint
            self.lastCheckpointPlayerPosition = [game.player.x,game.player.y]
            self.lastCheckpointMapName = game.currentRoom
            
        #     self.playerPosition[0] = game.player.x
        #     self.playerPosition[1] = game.player.y
        #     self.level = game.currentRoom
            

    def loadCheckpoint(self,game):
        if self.lastCheckpoint != None and self.lastCheckpointPlayerPosition != None and \
            self.lastCheckpointMapName != None:
            game.loadLevel(self.lastCheckpointMapName,game.objects,game.enemies,game.objectsTopLayer,game.objectsWaterLayer,(self.lastCheckpointPlayerPosition[0],self.lastCheckpointPlayerPosition[1]),False)
            game.player.x = self.lastCheckpointPlayerPosition[0]
            game.player.y = self.lastCheckpointPlayerPosition[1]
        else:
            game.loadLevel('1979',game.objects,game.enemies,game.objectsTopLayer,(64,96),False)