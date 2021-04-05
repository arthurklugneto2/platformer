import pygame
from pygame import Rect
from Modules.ui_message import UIMessage
from Modules.ui_dialog import UIDialog
from Modules.lang import Lang
import math

class UISystem:

    def __init__(self,screenSize,screenScale):
        self.scale = screenScale
        self.screenSize = screenSize
        self.defaultFont = pygame.font.Font("./Assets/Fonts/default.ttf", 16*screenScale)
        self.displayFont = pygame.font.Font("./Assets/Fonts/display.ttf", 16*screenScale)

        self.pathPrefix = './Assets/UI/'

        self.dialogTimerReset = 60
        self.dialogTimer = 60

        self.bgRectangle = pygame.Surface((screenSize[0],30*screenScale))
        self.bgRectangle.set_alpha(220)
        self.bgRectangle.fill((0,0,0))

        self.messageRectangle = pygame.Surface((400*screenScale,40*screenScale))
        self.messageRectangle.set_alpha(220)
        self.messageRectangle.fill((0,0,0))
        
        self.dialogRectangle = pygame.Surface((400*screenScale,200*screenScale))
        self.dialogRectangle.set_alpha(30)
        self.dialogRectangle.fill((255,255,255))

        self.keyIcon = pygame.image.load(self.pathPrefix+'key.png')
        self.coinIcon = pygame.image.load(self.pathPrefix+'coins.png')
        self.hearthIcon = pygame.image.load(self.pathPrefix+'hearth.png')
        self.hearthEmptyIcon = pygame.image.load(self.pathPrefix+'hearth_empty.png')

        self.hearthIcon = pygame.transform.scale( self.hearthIcon , (16*screenScale,12*screenScale) )
        self.hearthEmptyIcon = pygame.transform.scale( self.hearthEmptyIcon , (16*screenScale,12*screenScale) )
        self.keyIcon = pygame.transform.scale( self.keyIcon , (16*screenScale,22*screenScale) )
        self.coinIcon = pygame.transform.scale( self.coinIcon , (14*screenScale,20*screenScale) )

        self.messages = []
        self.dialogs = []

    def update(self,game,keys):

        # Black Rectangle
        game.display.blit( self.bgRectangle , (0,game.screenSize[1]-(30*self.scale)) )

        # Player Keys
        keys_number = self.defaultFont.render(str(game.player.keys),False,(255,255,255))
        game.display.blit(keys_number,(game.screenSize[0]-(36*self.scale),game.screenSize[1]-(26*self.scale)))
        game.display.blit(self.keyIcon,(game.screenSize[0]-(60*self.scale),game.screenSize[1]-(26*self.scale)))

        # Player Coins
        coins_number = self.defaultFont.render(str(game.player.coins),False,(255,255,255))
        game.display.blit(coins_number,(game.screenSize[0]-(126*self.scale),game.screenSize[1]-(26*self.scale)))
        game.display.blit(self.coinIcon,(game.screenSize[0]-(150*self.scale),game.screenSize[1]-(25*self.scale)))

        # Player Health
        lives_number = self.defaultFont.render(str(game.player.lives),False,(255,255,255))
        game.display.blit(lives_number,(10,game.screenSize[1]-(26*self.scale)))
        healthCalc = game.player.health
        for x in range( game.player.maxHealth ):
            if healthCalc > 0:
                game.display.blit(self.hearthIcon,(x * 20 * self.scale +(38* self.scale),game.screenSize[1]-(21*self.scale)))
            else:
                game.display.blit(self.hearthEmptyIcon,(x * 20*self.scale +(38* self.scale),game.screenSize[1]-(21*self.scale)))
            healthCalc -= 1

        # Display UI Messages
        if len(self.messages) > 0:
            if self.messages[0].time == 0:
                self.messages.pop(0)
            else:
                game.display.blit( self.messageRectangle , ((50* self.scale),game.screenSize[1]-(80* self.scale)) )
                text_message = self.defaultFont.render(self.messages[0].message,False,(255,255,255))
                game.display.blit(text_message,((64* self.scale),game.screenSize[1]-(72* self.scale)))
                self.messages[0].time -= 1

        if len(self.dialogs) > 0 and len(self.messages) == 0:

            dialog = self.dialogs[0]
            
            par0 = ''
            par1 = ''
            par2 = ''
            message = dialog.message

            if '|' in dialog.message:
                args = dialog.message.split('|')
                message = args[0]
                if len(args) == 2 :
                    par0 = game.switchSystem.getSwitch(args[1])
                if len(args) == 3 :
                    par0 = game.switchSystem.getSwitch(args[1])
                    par1 = game.switchSystem.getSwitch(args[2])
                if len(args) == 4 :
                    par0 = game.switchSystem.getSwitch(args[1])
                    par1 = game.switchSystem.getSwitch(args[2])
                    par2 = game.switchSystem.getSwitch(args[3])

            dialogText = str(Lang.__(message,par0,par1,par2))
            
            if not dialog.timeReset:
                dialog.timeReset = True
                self.dialogTimer = self.dialogTimerReset
            
            self.dialogRectangle.fill((178,148,122))
            game.display.blit(self.dialogRectangle,(50* self.scale,50* self.scale))
            self.dialogRectangle.fill((46,34,47))
            game.display.blit(self.dialogRectangle,(54* self.scale,54* self.scale))
            remainingText = self.drawText( game.display,dialogText,(199,220,208),Rect(60* self.scale,60* self.scale,380* self.scale,180* self.scale),self.defaultFont)
          
            game.display.blit(self.defaultFont
                .render(Lang.__('dialog.continue'),False,(0,0,0)),(60* self.scale,220* self.scale))
            if keys[pygame.K_e] and self.dialogTimer == 0:
                if remainingText != '':
                    self.dialogs.append(UIDialog(remainingText))
                self.dialogs.pop(0)

        #self.drawText(game.display,'ola',(0,0,0),Rect(0,0,200,200),self.defaultFont)

        self.dialogTimer -= 1
        if self.dialogTimer < 0: self.dialogTimer = 0

    def addMessage(self,message,time):
        self.messages.append( UIMessage(message,time) )

    def addDialog(self,message):
        messagesLine = message
        messages = messagesLine.split('|')
        dialogsQty = math.ceil(len(messages)/7)
        while len(messages) > 0:
            currentMessage = ''
            for x in range(7):
                if len(messages) > 0:
                    currentMessage += messages.pop(0)
                if x < 7 and len(messages) > 0:
                    currentMessage += '|'
            self.dialogs.append( UIDialog(currentMessage) )

    def hasDialog(self):
        return len(self.dialogs) > 0

    def drawText(self,surface, text, color, rect, font, aa=False, bkg=None):
        rect = Rect(rect)
        y = rect.top
        lineSpacing = -2

        # get the height of the font
        fontHeight = font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word      
            if i < len(text): 
                i = text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if bkg:
                image = font.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)

            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

        return text