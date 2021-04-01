import pygame
from os import listdir
from os.path import isfile, join
from Objects.sfx import SFX

class AudioSystem:

    def __init__(self):
        pygame.mixer.init()
        self.sfx = []
        sfxFiles = [f for f in listdir('./Assets/Audio/sfx/') if isfile(join('./Assets/Audio/sfx/', f))]
        self.loadEffects(sfxFiles)
        # pygame.mixer.music.load('./Assets/Audio/music/Track1.ogg')
        # pygame.mixer.music.play(-1, 0.0)
        # pygame.mixer.music.load('./Assets/Audio/music/Track2.ogg')
        # pygame.mixer.music.play(-1, 0.0)
        self.playMusic('Track1')

    def playMusic(self,name):
        pygame.mixer.music.load('./Assets/Audio/music/'+name+'.ogg')
        pygame.mixer.music.play(-1, 0.0)

    def playSFX(self,name):
        for sound in self.sfx:
            if sound.name == name+'.wav':
                sound.sound.play()
    
    def stopMusic(self):
        pygame.mixer.music.stop()

    def loadEffects(self,sfxFiles):
        path = './Assets/Audio/sfx/'
        for file in sfxFiles:
            self.sfx.append(SFX(file,pygame.mixer.Sound(path+file)))