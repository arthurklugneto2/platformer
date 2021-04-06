import pygame
from Objects.player import Player
from GameObjects.coin import Coin
from GameObjects.door import Door
from GameObjects.key import Key
from GameObjects.hearth import Hearth
from GameObjects.vine import Vine
from GameObjects.gate import Gate
from GameObjects.platform import Platform
from GameObjects.activation_block import ActivationBlock
from GameObjects.switch import Switch
from GameObjects.chest import Chest
from GameObjects.life import Life
from GameObjects.computer import Computer
from GameObjects.generalSwitch import GeneralSwitch
from GameObjects.display import Display
from GameObjects.puzzle import Puzzle
from Objects.ground import Ground
from Objects.water import Water
from Objects.background import Background
from Objects.box import Box
from Modules.collision import *
from Modules.animationSystem import AnimationSystem
from Modules.gameObjectSystem import GameObjectSystem
from Modules.enemySystem import EnemySystem
from Modules.switchSystem import SwitchSystem
from pytmx.util_pygame import load_pygame
from xml.dom import minidom

from Objects.quadTreeItem import QuadTreeItem
from Modules.Pyqtree import *
from Modules.Quadtree import *

# from GameObjects.coin import Coin

class Game:

    def __init__(self,player,objects,objectsWeapon,quadTree,objectsTopLayer,objectsWaterLayer,objectsOnce,enemies,buffer,display,screenSize,camera,animationSystem,gameObjectSystem,uiSystem,enemySystem,queueSystem,switchSystem,effectsSystem,saveSystem,audioSystem,playerSystem,puzzles,solvedPuzzles,activationPersist):
        
        self.player = player
        self.objects = objects
        self.objectsWeapon = objectsWeapon
        self.objectsTopLayer = objectsTopLayer
        self.objectsWaterLayer = objectsWaterLayer
        self.enemies = enemies
        self.quadTree = quadTree
        self.buffer = buffer
        self.display = display
        self.camera = camera

        self.animationSystem = animationSystem
        self.gameObjectSystem = gameObjectSystem
        self.objectsOnce = objectsOnce
        self.puzzles = puzzles
        self.solvedPuzzles = solvedPuzzles
        self.activationPersist = activationPersist
        self.queueSystem = queueSystem
        self.uiSystem = uiSystem
        self.enemySystem = enemySystem
        self.switchSystem = switchSystem
        self.effectsSystem = effectsSystem
        self.saveSystem = saveSystem
        self.audioSystem = audioSystem
        self.playerSystem = playerSystem
        
        self.screenSize = screenSize
        self.currentRoom = ''
        self.activatedCheckpoints = []

        self.counter = 0

    def update(self,keys):
        self.animationSystem.update()
        self.uiSystem.update(self,keys)
        self.queueSystem.update(self,self.uiSystem)
        self.playerSystem.update(self,keys)
        self.camera.update(self.player)
        self.counter += 1

    def findPropertyForXY(self,x,y,properties):
        location = str(x)+','+str(y)
        if location in properties:
            return properties[location]

    def loadLevel(self,levelName,objects,enemies,objectTopLayer,objectsWaterLayer,playerPosition,isRunME):

        playerInitialPositionCode = '1152'
        self.currentRoom = levelName
        levelName += '.tmx'

        objects.clear()
        objectTopLayer.clear()
        objectsWaterLayer.clear()
        enemies.clear()
        self.player.game = self
        objects.append(self.player)
        self.effectsSystem.effects.clear()
        self.player.x = playerPosition[0]
        self.player.y = playerPosition[1]

        prefix = './Assets/Levels/'
        tiled_map = load_pygame(prefix+levelName)
        mapWidth = tiled_map.width
        mapHeight = tiled_map.height

        # Map Tiles
        for layer in tiled_map.visible_layers:
            for x, y, image, in layer.tiles():
                if layer.name == "BG":
                    objects.append(Background(x * tiled_map.tilewidth, y * tiled_map.tileheight,
                                            tiled_map.tilewidth, tiled_map.tileheight, image))

                if layer.name == "DT":
                    objects.append(Background(x * tiled_map.tilewidth, y * tiled_map.tileheight,
                                            tiled_map.tilewidth, tiled_map.tileheight, image))
                
                elif layer.name == "TR":
                    objects.append(Ground(x * tiled_map.tilewidth, y * tiled_map.tileheight,
                                        tiled_map.tilewidth, tiled_map.tileheight, image))
        
                elif layer.name == "OL":
                    objectTopLayer.append(Ground(x * tiled_map.tilewidth, y * tiled_map.tileheight,
                                        tiled_map.tilewidth, tiled_map.tileheight, image))

                elif layer.name == "WA":
                    if image != None:
                        objectsWaterLayer.append(Water(x * tiled_map.tilewidth, y * tiled_map.tileheight,
                                            tiled_map.tilewidth, tiled_map.tileheight, image))

        mydoc = minidom.parse(prefix+levelName)

        # Water Surface
        dataXml = mydoc.getElementsByTagName('data')
        waterData = dataXml[6].firstChild.data.replace('\n','')
        waterDataArray = waterData.split(',')
        for index in range( len(waterDataArray) ):
            x = int(index % mapWidth);   
            y = int(index / mapWidth);
            tileSize = 32

            if waterDataArray[index] != '0':
                data = waterDataArray[index]
                waterSurfaceObject = self.gameObjectSystem.createGameObject(data,None,self,x * tileSize,y * tileSize,tileSize,tileSize)
                if waterSurfaceObject != None:
                    self.objectsTopLayer.append(waterSurfaceObject)

        # Game Objects
        dataXml = mydoc.getElementsByTagName('data')
        objectData = dataXml[3].firstChild.data.replace('\n','')
        objectDataArray = objectData.split(',')

        for index in range( len(objectDataArray) ):
            x = int(index % mapWidth);   
            y = int(index / mapWidth);
            tileSize = 32

            if objectDataArray[index] != '0':
                data = objectDataArray[index]

                # if executed in ME
                if data == playerInitialPositionCode:
                    self.player.x = x*32
                    self.player.y = y*32

                props = self.findPropertyForXY(x,y,tiled_map.layers[3].properties)
                gameObject = self.gameObjectSystem.createGameObject(data,props,self,
                    x * tileSize,y * tileSize,tileSize,tileSize)
                if gameObject != None:
                    if props != None:
                        if gameObject.have('once'):
                            if [self.currentRoom,x,y] not in self.objectsOnce:
                                self.objects.append(gameObject)
                        else:
                            self.objects.append(gameObject)
                    else:
                        self.objects.append(gameObject)

        
        self.quadTree = QuadTree(8,10000,10000)
        for obj in self.objects:
            if isinstance(obj, Ground) or isinstance(obj, GameObject):
                self.quadTree.add(RectData(obj.x,obj.y,obj.x+obj.w,obj.y+obj.h,obj))
        
        for obj in self.objectsWaterLayer:
            if isinstance(obj, Water) or isinstance(obj, WaterSurface):
                self.quadTree.add(RectData(obj.x,obj.y,obj.x+obj.w,obj.y+obj.h,obj))

        # Enemies
        enemiesData = dataXml[4].firstChild.data.replace('\n','')
        enemiesDataArray = enemiesData.split(',')

        for index in range( len(enemiesDataArray) ):
            x = int(index % mapWidth);   
            y = int(index / mapWidth);
            tileSize = 32

            data = enemiesDataArray[index]
            props = self.findPropertyForXY(x,y,tiled_map.layers[4].properties)
            enemy = self.enemySystem.createEnemy(data,props,self,
                x * tileSize,y * tileSize,tileSize,tileSize)
            if enemy != None:
                enemies.append( enemy )

    def countCoins(self):  
        coins = 0
        for obj in self.objects:
            if isinstance(obj,Coin):
                coins += 1
        return coins
    
    def countEnemies(self):
        return len(self.enemies)

    def getQuadTreeItens(self):
        # itens = self.quadTree.hit(QuadTreeItem(
        #     self.player.x,self.player.y,
        #     self.player.x+self.player.w,
        #     self.player.y+self.player.h))
        # return itens
        
        # overlapbbox = (self.player.x, self.player.y, 
        #                 self.player.x+self.player.w,
        #                 self.player.y+self.player.h)
        # matches = self.quadTree.intersect(overlapbbox)
        # return matches
        selected = [rect.data for rect in self.quadTree.querry(self.player.x,self.player.y,
             self.player.x+self.player.w,
             self.player.y+self.player.h)]
        return selected

    def removeQuadTreeItem(self,obj):
        selected = [rect for rect in self.quadTree.querry(self.player.x,self.player.y,
             self.player.x+self.player.w,
             self.player.y+self.player.h)]
        for select in selected:
            if select.data == obj:
                self.quadTree.remove(select)

    def getObjectAt(self,x,y):
        for obj in self.objects:
            if isinstance(obj,GameObject):
                if obj.x == x:
                    if obj.y == y:
                        return obj
        return None
    
    def addEnemy(self,enemy):
        enemyParts = enemy.split('|')
        enemyName = enemyParts[0]
        enemyPositionX = self.get('pX',enemy)
        enemyPositionY = self.get('pY',enemy)
        enemyAddParams = ''
        enemyCode = 0
        tileSize = 32

        if enemyName == 'slime':
            enemyCode = self.enemySystem.codeSlime
            enemyX = self.get('x',enemy)
            enemyY = self.get('y',enemy)
            enemyAddParams += 'x:'+enemyX+','
            enemyAddParams += 'y:'+enemyX+''

        if enemyName == 'bat':
            enemyCode = self.enemySystem.codeBat

        enemy = self.enemySystem.createEnemy(enemyCode,enemyAddParams,self,
                int(enemyPositionX) * tileSize,int(enemyPositionY) * tileSize,tileSize,tileSize)
        if enemy != None:
            self.enemies.append( enemy )

    def get(self,name,item):
        parts = item.split('|')
        for part in parts:
            partParams = part.split('-')
            if partParams[0] == name:
                return partParams[1]
        return None