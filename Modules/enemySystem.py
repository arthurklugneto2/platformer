from Enemies.slime import Slime
from Enemies.spike import Spike
from Enemies.bat import Bat
from Modules.queue_item import QueueItem
import random

class EnemySystem:

    def __init__(self):
        n = 1153
        self.codeSlime = str(n)
        self.codeSpike = str(n+1)
        self.codeBat = str(n+2)

    def createEnemy(self,code,props,game,x,y,w,h):
        
        if code != '0':  
            if code == self.codeSlime:
                return Slime(x,y,w,h,props,game)
            if code == self.codeSpike:
                return Spike(x,y,w,h,props,game)
            if code == self.codeBat:
                return Bat(x,y,w,h,props,game)
                            
        return None

    def enemyDefaultDrop(self,enemy):

        if isinstance(enemy,Slime):
            return self.slimeDefaultDrop()

    def slimeDefaultDrop(self):
        lotery = random.uniform(0, 1)
        if lotery < .05:
            return QueueItem('GIVE_PLAYER','HEARTH:1')
