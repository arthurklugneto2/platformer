class SwitchSystem:

    def __init__(self):
        self.switches = {}

    def setSwitch(self, name, value):
        self.switches[name] = value

    def clearSwitch(self,name):
        self.switches.pop(name,None)

    def hasSwitch(self,name):
        return name in self.switches

    def getSwitch(self,name):
        if self.hasSwitch(name):
            return self.switches[name]
        else:
            return ''