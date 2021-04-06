import pygame
import sys
from Screens.screen import Screen
from Objects.player import Player
from Objects.enemy import Enemy
from Enemies.slime import Slime
from GameObjects.vine import Vine
from Objects.ground import Ground
from Objects.background import Background
from Objects.box import Box
from Objects.camera import Camera
from Modules.lang import Lang
from Modules.collision import *
from Modules.animationSystem import AnimationSystem
from Modules.gameObjectSystem import GameObjectSystem
from Modules.queueSystem import QueueSystem
from Modules.enemySystem import EnemySystem
from Modules.uiSystem import UISystem
from Modules.switchSystem import SwitchSystem
from Modules.effectsSystem import EffectsSystem
from Modules.saveSystem import SaveSystem
from Modules.audioSystem import AudioSystem
from Modules.playerSystem import PlayerSystem
from Modules.game import Game
from pytmx.util_pygame import load_pygame
from xml.dom import minidom
from Enemies.slime import Slime
from Modules.Pyqtree import *

class GameScreen(Screen):

    def __init__(self):
        self.name = "GAME_SCREEN"
    
    def create(self,buffer,display,screenSize,screenScale):
        self.createGameObjects()
        self.createPlayer()
        self.createGame(buffer,display,screenSize,screenScale)

        self.loadInitialMap()

    def createGameObjects(self):
        self.objects = []
        self.objectsTopLayer = []
        self.objectsWaterLayer = []
        self.objectsOnce = []
        self.objectsWeapon = []

        self.puzzles = []
        self.solvedPuzzles = []
        self.enemies = []
        self.elements = []
        self.activationPersist = []

        self.quadTree = None
        self.needUpdate = True
        self.camera = Camera(0,0)
    
    def createPlayer(self):
        player_width = 32
        player_height = 32
        self.player = Player(0,0, player_width, player_height)

    def createGame(self,buffer,display,screenSize,screenScale):
        self.game = Game(self.player,self.objects,self.objectsWeapon,self.quadTree,self.objectsTopLayer,self.objectsWaterLayer,self.objectsOnce,
            self.enemies,buffer,display,screenSize,
            self.camera,AnimationSystem(),GameObjectSystem(),
            UISystem(screenSize,screenScale),EnemySystem(),QueueSystem(),SwitchSystem(),EffectsSystem(),
            SaveSystem(),AudioSystem(),PlayerSystem(self.player),self.puzzles,self.solvedPuzzles,self.activationPersist)

    def loadInitialMap(self):
        arguments = sys.argv
        commandMapName = None
        commandMap = False
        if len(arguments) == 4:
            if '-R' in arguments:
                mapFile = arguments[2]
                mapPath = arguments[3]
                commandMapName = mapFile.replace(mapPath,'').replace('.tmx','').replace('/','')

        levelName = '1979'
        levelPos = [2,3]
        # levelName = '39C4'
        # levelPos = [13,2]

        if commandMapName != None:
            levelName = commandMapName
            commandMap = True
            levelPos[0] = 0
            levelPos[1] = 0

        initialLoction = (levelPos[0] * 32,levelPos[1] * 32)

        self.game.loadLevel(levelName,self.objects,self.enemies,self.objectsTopLayer,self.objectsWaterLayer,initialLoction,commandMap)
        if self.game.saveSystem.hasSaveFile() and not commandMap:
            self.game.saveSystem.loadGame(self.game)

    def update(self,keys):

        if not self.game.uiSystem.hasDialog() or self.needUpdate:
            
            # Update Game Objects
            for obj in self.objects:
                obj.update(keys)

            # Update Enemies
            for enemy in self.enemies:
                enemy.update(keys)

            # If there is Puzzle
            # update the puzzle
            for puzzle in self.puzzles:
                puzzle.update(keys)

            # Perform Collision Calculations
            for obj in self.game.getQuadTreeItens():
                if not isinstance(obj, Player) and obj.collide:
                    player_check(self.objects[0], obj,self.game)
                
            for enemy in self.enemies:
                    enemy_check(enemy,self.objects[0],self.game)

            # Update weapons objects such as bullets, etc
            for weapon in self.objectsWeapon:
                weapon.update()
                bullet_check(weapon,self.game)
                if weapon.life <= 0:
                    self.objectsWeapon.remove(weapon)

            self.game.effectsSystem.update()

    def draw(self,buffer,display,screenSize,keys):
        if not self.game.uiSystem.hasDialog() or self.needUpdate:
            buffer.fill((0,0,0))

            # Draw Game Objects
            for obj in self.objects:
                if not isinstance(obj, Player):
                    obj.draw(buffer,self.camera)

            # Draw Player
            self.objects[0].draw(buffer,self.camera)

            # Draw Enemies
            for enemy in self.enemies:
                enemy.draw(buffer,self.camera)

            # Draw Puzzles
            for puzzle in self.puzzles:
                puzzle.draw(buffer,self.camera)

            # Draw objects in Top Layer
            for obj in self.objectsTopLayer:
                if not isinstance(obj, Player):
                    obj.draw(buffer,self.camera)

            # Draw objects in Water
            for obj in self.objectsWaterLayer:
                if not isinstance(obj, Player):
                    obj.draw(buffer,self.camera)

            for weapon in self.objectsWeapon:
                weapon.draw(buffer,self.camera)

            # Draw Game Effetcs
            self.game.effectsSystem.draw(buffer,self.camera)

            # Transfer Buffer to Display
            display.blit(pygame.transform.scale(buffer, screenSize), (0, 0))

            self.needUpdate = False
        
        self.game.update(keys)

    def destroy(self):
        pass
    