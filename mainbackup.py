'''
    Imports
'''
import pygame
import sys
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
from Modules.game import Game
from pytmx.util_pygame import load_pygame
from xml.dom import minidom
from Enemies.slime import Slime
from Modules.Pyqtree import *

pygame.init()
pygame.font.init()

'''
    Globals e Settings
'''
DEBUG_MODE = False


# Display
WIDTH = 512
HEIGHT = 320
SCALE = 1

display_width = WIDTH
display_height = HEIGHT
display = pygame.display.set_mode((display_width, display_height))
buffer = pygame.Surface((int(WIDTH/SCALE),int(HEIGHT/SCALE)))
clock = pygame.time.Clock()
camera = Camera(0,0)
objects = []
objectsTopLayer = []
objectsWaterLayer = []
objectsOnce = []
quadTree = None
puzzles = []
solvedPuzzles = []
enemies = []
elements = []
activationPersist = []
gameState = 2
needUpdate = True

# Player
player_width = 32
player_height = 32
player = Player(0,0, player_width, player_height)

# Application Status
applicationDone = False

# font
# uiFont = pygame.font.Font("./Assets/Fonts/default.ttf", 16)

'''
    Systems
'''
game = Game(player,objects,quadTree,objectsTopLayer,objectsWaterLayer,objectsOnce,
        enemies,buffer,display,(display_width,display_height),
        camera,AnimationSystem(),GameObjectSystem(),
        UISystem(),EnemySystem(),QueueSystem(),SwitchSystem(),EffectsSystem(),
        SaveSystem(),AudioSystem(),puzzles,solvedPuzzles,activationPersist)

'''
    Run From ME
'''
# main.py -R %mapfile %mappath
arguments = sys.argv
commandMapName = None
commandMap = False
if len(arguments) == 4:
    if '-R' in arguments:
        mapFile = arguments[2]
        mapPath = arguments[3]
        commandMapName = mapFile.replace(mapPath,'').replace('.tmx','').replace('/','')

'''
    Load Initial Map
'''
levelName = '1979'
levelPos = [2,3]
#levelName = 'D1CD'
#levelPos = [21,7]

if commandMapName != None:
    levelName = commandMapName
    commandMap = True
    levelPos[0] = 0
    levelPos[1] = 0

initialLoction = (levelPos[0] * 32,levelPos[1] * 32)
game.loadLevel(levelName,objects,enemies,objectsTopLayer,objectsWaterLayer,initialLoction,commandMap)

while not applicationDone:

    clock.tick(60)
    keys = pygame.key.get_pressed()

    event = pygame.event.get()

    for e in event:
        if e.type == pygame.QUIT:
            applicationDone = True

    if gameState == 2:  # PLay Game

        if not game.uiSystem.hasDialog() or needUpdate:

            '''
                UPDATE
            '''
            buffer.fill((0,0,0))

            # Update the GameObjects
            for obj in objects:
                obj.update(keys)
                
            # Update the Enemies
            for enemy in enemies:
                enemy.update(keys)

            # If there is Puzzle
            # update the puzzle
            for puzzle in puzzles:
                puzzle.update(keys)
                
            '''
                COLLISION
            '''
            for obj in game.getQuadTreeItens():
                if not isinstance(obj, Player) and obj.collide:
                    player_check(objects[0], obj,game)
                
            for enemy in enemies:
                    enemy_check(enemy,objects[0],game)

            '''
                Effects System
            '''
            game.effectsSystem.update()

            '''
                Draw
            '''
            # Draw Objects
            for obj in objects:
                if not isinstance(obj, Player):
                    obj.draw(buffer,camera)
            objects[0].draw(buffer,camera)

            # Draw Enemies
            for enemy in enemies:
                enemy.draw(buffer,camera)

            # Draw Puzzles
            for puzzle in puzzles:
                puzzle.draw(buffer,camera)

            # Draw objects in Top Layer
            for obj in objectsTopLayer:
                if not isinstance(obj, Player):
                    obj.draw(buffer,camera)

            # Draw objects in Top Layer
            for obj in objectsWaterLayer:
                if not isinstance(obj, Player):
                    obj.draw(buffer,camera)

            # Draw the Buffer to the Screen
            game.effectsSystem.draw(buffer,camera)
            display.blit(pygame.transform.scale(buffer, (WIDTH,HEIGHT)), (0, 0))

            needUpdate = False

    if keys[pygame.K_F4]:
        game.saveSystem.loadCheckpoint(game)

    game.update(keys)
    pygame.display.flip()