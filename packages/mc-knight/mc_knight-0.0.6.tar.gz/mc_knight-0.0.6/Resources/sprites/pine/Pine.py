import random
import pygame
import sys
import os
from pygame.locals import *
from Resources.sprites.sprite import Sprite
class Pine(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        n=0
        for x in range(4):
            self.element.append(pygame.image.load(Get('pine_' + str(n) + '.png')))
            n+=1
    def GetElement(self):
        return self.element[random.randint(0,3)]

def Get(name):
    return os.path.dirname(os.path.realpath(__file__))+"\\"+name
