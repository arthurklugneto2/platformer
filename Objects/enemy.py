import pygame
from pygame.math import Vector2
from Modules.mathFunctions import MathFunctions

class Enemy:

    def __init__(self,x,y,w,h,props,game):
        self.properties = None
        self.position = Vector2(x,y)
        self.velocity = Vector2()
        self.acceleration = Vector2()
        self.maxSpeed = 1.5

    def draw(self, display,camera):
        pass

    def update(self, keys):
        self.velocity += self.acceleration
        self.velocity = MathFunctions.limitVector(self.velocity,self.maxSpeed)
        self.position += self.velocity
        self.acceleration.update(0,0)

    def setProperties(self,props):
        if props == None:
            self.properties = None
        else:
            self.properties = props.split(',')

        # all keys to lowercase
        if self.properties != None:
            for x in range(len(self.properties)):
                if ':' in self.properties[x]:
                    parts = self.properties[x].split(':')
                    self.properties[x] = parts[0].lower()+':'+parts[1]
                else:
                    self.properties[x] = self.properties[x].lower()

    def have(self,name):
        if self.properties != None:
            for x in range(len(self.properties)):
                prop = self.properties[x]
                if ':' in prop:
                    propParts = prop.split(':')
                    if propParts[0] == name : return True
                else:
                    if prop == name : return True
        return False

    def get(self,name):
        if self.properties != None:
            for x in range(len(self.properties)):
                prop = self.properties[x]
                if ':' in prop:
                    propParts = prop.split(':')
                    if propParts[0] == name : return propParts[1]
                elif prop == name:
                    return True
        return None

    def getMany(self,name):
        values = []
        if self.properties != None:
            for x in range(len(self.properties)):
                prop = self.properties[x]
                if ':' in prop:
                    propParts = prop.split(':')
                    if propParts[0] == name : values.append(propParts[1])
                else:
                    continue
        return values