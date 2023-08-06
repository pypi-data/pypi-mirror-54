from Script.Layer.Layer import Layer
from Resources.sprites.water.Water import Water
from Script.assist.Array import Array
import pygame
from pygame.locals import *
class WaterLayer(Layer):
    def __init__(self,cols,rows,array,grass,collider):
        Layer.__init__(self,cols,rows)
        self.array=Array()
        self.array.Set(array)
        self.element=Water()
        self.CreateLayer(grass,collider)
    def CreateLayer(self,grass,collider):
        for i in range(self.cols):
            for j in range(self.rows):
                if self.array[i,j]!=0:
                    collider[i,j]=1
                    if self.array[i,j] == 2:
                        grass.myLayer[i,j]=pygame.transform.rotate(self.element.GetElement(),180)
                    else:
                        grass.myLayer[i,j]=self.element.GetElement()