class Camera:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.playerOffset = (220,180)

    def update(self,player):
        self.x = int(-player.x + self.playerOffset[0])
        self.y = int(-player.y + self.playerOffset[1])