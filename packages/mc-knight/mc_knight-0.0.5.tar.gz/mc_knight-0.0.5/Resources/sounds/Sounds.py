
import random
import pygame
import sys
import os
from pygame.locals import *
from Resources.sprites.sprite import Sprite
class Sounds(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        n=0
        self.element.append(Get('sound_' + str(n) + '.mp3'))
    def GetEement(self):
        return self.element[0]

def Get(name):
    return os.path.dirname(os.path.realpath(__file__))+"\\"+name



