from Screens.game_Screen import GameScreen

class ScreenSystem(object):

    def __init__(self):
        # Setup all all available screens
        self.currentScreen = None
        self.screens = []

        # Game Screen
        self.screens.append( GameScreen() )

    def loadScreeen(self,name,buffer,display,screenSize,scale):
        if self.currentScreen != None:
            self.currentScreen.destroy()
            self.currentScreen = None

        newScreen = self.getScreenByName(name)
        if newScreen != None:
            self.currentScreen = newScreen
            newScreen.create(buffer,display,screenSize,scale)

    def getScreenByName(self,name):
        for x in self.screens:
            if x.name == name:
                return x
        return None        

    def update(self,keys):
        if self.currentScreen != None:
            self.currentScreen.update(keys)

    def draw(self,buffer,display,screenSize,keys):
        if self.currentScreen != None:
            self.currentScreen.draw(buffer,display,screenSize,keys)


