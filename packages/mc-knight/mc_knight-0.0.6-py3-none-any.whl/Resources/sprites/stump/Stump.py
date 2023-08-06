import random
import pygame
import sys
import os
from pygame.locals import *
from Resources.sprites.sprite import Sprite
class Stump(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        n=0
        self.element.append(pygame.image.load(Get('stump_' + str(n) + '.png')))
    def GetElement(self):
        return self.element[0]

def Get(name):
    return os.path.dirname(os.path.realpath(__file__))+"\\"+name
