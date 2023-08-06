import random
import pygame
from pygame.locals import *
import sys
import os
from Resources.sprites.sprite import Sprite

class Water:
    def __init__(self):
        Sprite.__init__(self)
        n=0
        for x in range(3):
            self.element.append(pygame.image.load(Get('water_' + str(n) + '.png')))
            n+=1
    def GetElement(self):
        return self.element[random.randint(0,2)]

def Get(name):
    return os.path.dirname(os.path.realpath(__file__))+"\\"+name
