import pygame
from Objects.quadTreeItem import QuadTreeItem

class GameObject(QuadTreeItem):

    def __init__(self):
        self.properties = None

    def draw(self, display,camera):
        pass

    def update(self, keys):
        pass

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