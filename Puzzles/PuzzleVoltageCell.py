import random
from Modules.lang import Lang
from GameObjects.puzzle import Puzzle
from GameObjects import *

class PuzzleVoltageCell(Puzzle):

    '''
        Puzzle : Voltage Cell

        Description : Player has to figure out the voltage in order to open
                      the cell. It operates buttons that add some value or
                      remove. Each button add a especific value. Based on
                      Myst voltage puzzle

        Switches :  P_1C11_target_voltage : The target puzzle solving voltage
                   P_1C11_current_voltage : The randomly generated voltage

        Button Values : 43,-13,61,-37,29,23,59,-19,47
    '''

    def __init__(self,x,y,w,h,properties,game):
        self.x = x
        self.y = y
        self.setProperties(properties)
        self.w = w
        self.h = h
        self.game = game
        self.name = 'puzzle_1c11'
        self.isSolved = False
        self.collide = False

        # Objects
        self.display = None
        self.sw = []
        self.gate = None
        self.gateX = 0
        self.gateY = 0

        self.primes = [43,-13,61,-37,29,23,59,-19,47]
        if self.have('primes'):
            self.primes = list(map(int,self.get('primes').split('|')))
        self.buttonsXOffset = 0
        if self.have('buttons_x'):
            self.buttonsXOffset = int(self.get('buttons_x'))

        if self.have('gate_x'):
            self.gateX = int(self.get('gate_x')) * 32
        if self.have('gate_y'):
            self.gateY = int(self.get('gate_y')) * 32

        self.switchSource = self.get('switch_source')
        self.switchTarget = self.get('switch_target')
        self.buttons = 5
        if self.have('buttons'):
            self.buttons = int(self.get('buttons'))

    def create(self):
        self.createSwitches()
        self.createDisplay()
        self.createButtons()
        self.creteActivationBlock()

    def createDisplay(self):
        code = self.game.gameObjectSystem.codeDisplay
        properties = 'size:3,value:0,sufix:V'
        self.display = self.game.gameObjectSystem.createGameObject(code,properties,self.game,self.x+2*32,self.y-3*32,16,16)
        self.game.objects.append(self.display)

    def createSwitches(self):
        self.game.switchSystem.setSwitch(self.switchSource,0)
        if not self.game.switchSystem.hasSwitch(self.switchTarget):
            self.game.switchSystem.setSwitch(self.switchTarget,self.generateRandomVoltage())

    def createButtons(self):
        code = self.game.gameObjectSystem.codeGeneralSwitch

        for x in range(self.buttons):
            self.sw.append(self.game.gameObjectSystem.createGameObject(code,'color:blue,skin:3',self.game,self.x + (x*48)+self.buttonsXOffset,self.y,16,16))
            self.game.objects.append(self.sw[x])

    def creteActivationBlock(self):
        code = self.game.gameObjectSystem.codeActivationBlock
        self.gate = self.game.gameObjectSystem.createGameObject(code,None,self.game,
                    self.x+self.gateX,self.y+self.gateY,16,16)
        self.game.objects.append(self.gate)

    def generateRandomVoltage(self):
        value = 0
        while value == 0:
            for x in range(self.buttons):
                if random.choice([True, False]):
                    value += self.primes[x]
        return value

    def solved(self):
        source = self.game.switchSystem.getSwitch(self.switchSource)
        target = self.game.switchSystem.getSwitch(self.switchTarget)

        self.isSolved = int(source) == int(target)

        if self.name in self.game.solvedPuzzles:
            self.isSolved = True

        if self.isSolved:
            for button in self.sw:
                button.enabled = False 
            self.game.removeQuadTreeItem(self.gate)
            if self.gate in self.game.objects:
                self.game.objects.remove(self.gate)
            if self.name not in self.game.solvedPuzzles:
                self.game.solvedPuzzles.append(self.name)

    def draw(self, display,camera):
        pass

    def update(self, keys):

        sum = 0
        for x in range(self.buttons):
            if self.sw[x].isActivated: sum += self.primes[x]
        self.game.switchSystem.setSwitch(self.switchSource,sum)

        if not self.isSolved:
            self.display.value = str(sum)
        else:
            self.display.prefix = ''
            self.display.sufix = ''
            self.display.value = Lang.__('puzzle_1C11_display_open')

        #check if it is solved
        self.solved()

    