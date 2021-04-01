import random
from Modules.lang import Lang
from GameObjects.puzzle import Puzzle
from GameObjects import *

class PuzzleLevers(Puzzle):

    def __init__(self,x,y,w,h,properties,game):
        self.x = x
        self.y = y
        self.setProperties(properties)
        self.w = w
        self.h = h
        self.game = game
        self.name = 'puzzle_aa6c'
        self.isSolved = False
        self.executedSolveLogic = False
        self.collide = False

        if self.name in self.game.solvedPuzzles:
            self.isSolved = True

        self.light = None
        self.sw = []

        self.lightX = 0
        if self.have('light_x'):
            self.lightX = int(self.get('light_x'))
        self.lightY = 0
        if self.have('light_y'):
            self.lightY = int(self.get('light_y'))
        self.buttons = 5
        if self.have('buttons'):
            self.buttons = int(self.get('buttons'))
        self.buttonsXOffset = 0
        if self.have('buttons_x'):
            self.buttonsXOffset = int(self.get('buttons_x'))

    def create(self):
        self.createLight()
        self.createButtons()

    def createLight(self):
        code = self.game.gameObjectSystem.codeLight
        self.light = self.game.gameObjectSystem.createGameObject(code,'',self.game,self.x+self.lightX,self.y+self.lightY,32,32)
        self.game.objects.append(self.light)

    def createButtons(self):
        code = self.game.gameObjectSystem.codeGeneralSwitch

        for x in range(self.buttons):
            sw = self.game.gameObjectSystem.createGameObject(code,'color:blue,skin:3',self.game,self.x + (x*32)+self.buttonsXOffset,self.y,16,16)
            active = x % 2 == 1
            sw.isActivated = active
            self.sw.append(sw)
            self.game.objects.append(self.sw[x])

    def solved(self):
        if not self.isSolved:
            solved = True
            for sws in self.sw:
                if not sws.isActivated:
                    solved = False
            self.isSolved = solved
    
        if self.name in self.game.solvedPuzzles:
            self.isSolved = True
            self.light.isActivated = True
            for x in self.sw:
                x.isActivated = True

        if self.isSolved and not self.executedSolveLogic:
            if not self.name in self.game.solvedPuzzles:
                self.game.solvedPuzzles.append(self.name)
            self.executedSolveLogic = True

    def draw(self, display,camera):
        pass

    def update(self, keys):

        for x in range(len(self.sw)):
            if self.sw[x].hasUpdated and x == 0:
                self.sw[1].isActivated = not self.sw[1].isActivated
            elif self.sw[x].hasUpdated and x == len(self.sw)-1:
                self.sw[len(self.sw)-2].isActivated = not self.sw[len(self.sw)-2].isActivated
            else:
                if self.sw[x].hasUpdated:
                    self.sw[x-1].isActivated = not self.sw[x-1].isActivated
                    self.sw[x+1].isActivated = not self.sw[x+1].isActivated
                    pass

        for x in self.sw:
            if x.hasUpdated:
                x.hasUpdated = False        

        self.solved()
