from Script.Layer.GrassLayer import GrassLyaer
from Script.Layer.WaterLayer import WaterLayer
from Script.Layer.PineLayer import PineLayer
from Script.Layer.StoneLayer import StoneLayer
from Script.Layer.StumpLayer import StumpLayer
from Script.Layer.CastleLayer import CastleLayer
from Script.Layer.BackGroundLayer import BackGroundLayer
from Script.Layer.PlayerLayer import PlayerLayer
from Script.Layer.BlankLayer import BlankLayer
from Script.Layer.StumpLayer import StumpLayer
from Script.Layer.CollisionLayer import CollisionLayer
from Script.Layer.SoundsLayer import SoundsLayer
from Script.Layer.EquipageLayer import EquipageLayer
from Script.assist.Array import Array
import threading
import pygame
import time
from pygame.locals import *

class MixedLayer:
    _instance_lock = threading.Lock()
    def __init__(self,cols,rows):
        self.cols=cols
        self.rows=rows
        self.myLayer=Array()
        self.collider=CollisionLayer(cols,rows)
        self.grassLayer=GrassLyaer(self.cols,self.rows)
        self.substance=BlankLayer(self.cols,self.rows)
        self.layer=[]
        self.equList=[]
        self.colliderArray=Array(cols,rows)
        self.layer.append(self.grassLayer)
        self.layer.append(self.substance)
        self.sound=SoundsLayer()
        self.sound.CreateLayer()
        self.sound.PlaySound()
        self.CreateBackGround()
    def CreateBackGround(self):
        self.backGroundLayer=BackGroundLayer() 
    def CreateWater(self,array):
        self.waterLayer=WaterLayer(self.cols,self.rows,array,self.grassLayer,self.colliderArray)  
    def CreatePine(self,array):
        self.pineLayer=PineLayer(self.cols,self.rows,array,self.substance,self.colliderArray) 
    def CreateStone(self,array):
        self.stoneLayer=StoneLayer(self.cols,self.rows,array,self.substance,self.colliderArray) 
    def CreateStump(self,array):
        self.stumpLayer=StumpLayer(self.cols,self.rows,array,self.substance,self.colliderArray) 
    def CreateCastle(self,array):
        self.castleLayer=CastleLayer(self.cols,self.rows,array,self.substance,self.colliderArray) 
    def CreatePlayer(self,array):
        self.playerLayer=PlayerLayer(self.cols,self.rows,array)
    def CreateEquipage(self,array):
        self.EquipageLayer=EquipageLayer(self.cols,self.rows,array,self,self.colliderArray)
    def UpdateCollision(self):
        self.collider.UpdateCollision(self.colliderArray)
    def GetPlayer(self):
        return self.playerLayer.element
    def GetCollision(self):
        return self.collider.myLayer
    def StartMixed(self,screen):   
        while True:
            screen.blit(self.backGroundLayer.GetBackGround(),(0,0))
            for x in self:
                if x!=None:
                    self.myLayer.Set(x)
                    for i in range(0,x.cols):  
                        for j in range(x.rows):
                            a=int(j*65+(300-(x.rows/2*65))-10)
                            b=int(i*65+(300-(x.cols/2*65))+30)
                            if x.myLayer[i,j]:  
                                screen.blit(x.myLayer[i,j], (a,b))
                else:
                    break
            for x in self.equList:
                screen.blit(x.GetAnim(),(x.x,x.y))
            screen.blit(self.playerLayer.GetPlayer(),self.playerLayer.GetPlayerPos())
            time.sleep(1/30)
            pygame.display.update()
    @staticmethod
    def GetInstance():
        return MixedLayer._instance
    def __iter__(self):
        self.index=0
        return self
    def __next__(self):
        if self.index < len(self.layer):
            self.index+=1
            return self.layer[self.index-1]
        else:
            return None
    def __new__(cls, *args, **kwargs):
        if not hasattr(MixedLayer, "_instance"):
            with MixedLayer._instance_lock:
                if not hasattr(MixedLayer, "_instance"):
                    MixedLayer._instance = object.__new__(cls)  
        return MixedLayer._instance