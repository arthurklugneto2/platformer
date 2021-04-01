from Objects.effect import Effect

class EffectsSystem:

    def __init__(self):
        self.effects = []
        # self.effects.append(Effect(0,0,16,16,'./Assets/Objects/collected.png',True,5,10))

    def update(self):
        for effect in self.effects:
            effect.update(self)

    def draw(self,display,camera):
        for effect in self.effects:
            effect.draw(display,camera)

    def addEffect(self,effect):
        self.effects.append(effect)

    def generateEffect(self,name,x,y,offSetX = 0,offSetY = 0):
        
        if name == 'COLLECTED':
            self.effects.append(Effect(x+offSetX,y+offSetY,16,16,'./Assets/Objects/collected.png',False,5,5)) 
        if name == 'BAT_KILL':
            self.effects.append(Effect(x+offSetX,y+offSetY,16,16,'./Assets/Enemies/bat_kill.png',False,6,3))