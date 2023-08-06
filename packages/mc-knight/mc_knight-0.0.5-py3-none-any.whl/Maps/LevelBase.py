from Script.Layer.MixedLayer import MixedLayer
from Script.assist.Array import Array
from Script.Player.Knight import Knight
import _thread
import pygame
from pygame.locals import *
class LevelBase:
    def __init__(self,screen,cols,rows):      
        self.cols=cols
        self.rows=rows
        self.screen=screen
        self.mixedLayer=MixedLayer(cols,rows)
    def CreateWater(self,array):
        self.mixedLayer.CreateWater(array)
        print('添加河流')
    def CreatePine(self,array):
        self.mixedLayer.CreatePine(array)
        print('添加树木')
    def CreateStone(self,array):
        self.mixedLayer.CreateStone(array)
        print('添加石头')
    def CreateStump(self,array):
        self.mixedLayer.CreateStump(array)
        print('添加树墩')
    def CreateCastle(self,array):
        self.mixedLayer.CreateCastle(array)
        print('添加城堡')
    def CreatePlayer(self,array):
        self.mixedLayer.CreatePlayer(array)
        print('添加人物')
    def CreateEquipage(self,array):
        self.mixedLayer.CreateEquipage(array)
        print('添加道具')
    def UpdateCollision(self):
        self.mixedLayer.UpdateCollision()
        print('创建碰撞体')
    def LoadMap(self,screen):
        _thread.start_new_thread(self.mixedLayer.StartMixed,(screen,))
        #_thread.start_new_thread(self.player.Run,(screen,))
        #self.mixedLayer.StartMixed(screen)
        #self.player.forword()
    def GetPlayer(self):
        return self.knight
            
