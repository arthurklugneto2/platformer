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
from GameObjects.light import Light
from GameObjects.checkpoint import Checkpoint
from GameObjects.waterSurface import WaterSurface
from GameObjects.puzzle import Puzzle

from Puzzles.PuzzleVoltageCell import PuzzleVoltageCell
from Puzzles.PuzzleLevers import PuzzleLevers

class GameObjectSystem:

    def __init__(self):
        n = 1025
        self.codeCoin = str(n)
        self.codeDoor = str(n+1)
        self.codeHearth = str(n+2)
        self.codeKey = str(n+3)
        self.codeVine = str(n+4)
        self.codeGate = str(n+5)
        self.codeQuestionBlock = str(n+6)
        self.codeSwitch = str(n+7)
        self.codeChest = str(n+8)
        self.codePlatform = str(n+9)
        self.codeActivationBlock = str(n+10)
        self.codeLife = str(n+11)
        self.codeComputer = str(n+12)
        self.codeGeneralSwitch = str(n+13)
        self.codeDisplay = str(n+14)
        self.codeLight = str(n+15)
        self.codeCheckpoint = str(n+16)

        self.codePuzzle1 = str(n+126)
        self.codePuzzle2 = str(n+125)

        self.codeWSBlue = str(n+64)
        self.codeWSRed = str(n+65)
        self.codeWSGreen = str(n+66)
        self.codeWSGreen2 = str(n+67)
        self.codeWSCyan = str(n+68)
        self.codeWSPurple = str(n+69)
        self.codeWSPink = str(n+70)

    def createGameObject(self,code,props,game,x,y,w,h):
        
        if code != 0:
            
            # Reglar Objects
            if code == self.codeCoin:
                return Coin(x,y,w,h,props,game)
            elif code == self.codeDoor:
                return Door(x,y,w,h,props,game)
            elif code == self.codeKey:
                return Key(x,y,w,h,props,game)
            elif code == self.codeHearth:
                return Hearth(x,y,w,h,props,game)
            elif code == self.codeVine:
                return Vine(x,y,w,h,props,game)
            elif code == self.codeGate:
                return Gate(x,y,w,h,props,game)
            elif code == self.codePlatform:
                return Platform(x,y,w,h,props,game)
            elif code == self.codeActivationBlock:
                return ActivationBlock(x,y,w,h,props,game)
            elif code == self.codeSwitch:
                return Switch(x,y,w,h,props,game)
            elif code == self.codeChest:
                return Chest(x,y,w,h,props,game)
            elif code == self.codeLife:
                return Life(x,y,w,h,props,game)
            elif code == self.codeComputer:
                return Computer(x,y,w,h,props,game)
            elif code == self.codeGeneralSwitch:
                return GeneralSwitch(x,y,w,h,props,game)
            elif code == self.codeDisplay:
                return Display(x,y,w,h,props,game)
            elif code == self.codeLight:
                return Light(x,y,w,h,props,game)
            elif code == self.codeCheckpoint:
                return Checkpoint(x,y,w,h,props,game)

            #Water Surface
            elif code == self.codeWSBlue:
                return WaterSurface(x,y,w,h,'color:blue',game)
            elif code == self.codeWSRed:
                return WaterSurface(x,y,w,h,'color:red',game)
            elif code == self.codeWSGreen:
                return WaterSurface(x,y,w,h,'color:green',game)
            elif code == self.codeWSGreen2:
                return WaterSurface(x,y,w,h,'color:green2',game)
            elif code == self.codeWSCyan:
                return WaterSurface(x,y,w,h,'color:cyan',game)
            elif code == self.codeWSPurple:
                return WaterSurface(x,y,w,h,'color:purple',game)
            elif code == self.codeWSPink:
                return WaterSurface(x,y,w,h,'color:pink',game)

            #Puzzle
            elif code == self.codePuzzle1:
                puzzle = PuzzleVoltageCell(x,y,w,h,props,game)
                puzzle.create()
                return puzzle
            elif code == self.codePuzzle2:
                puzzle = PuzzleLevers(x,y,w,h,props,game)
                puzzle.create()
                return puzzle
                            
        return None