import pygame

from pygame.locals import *
from Script.Layer.MixedLayer import MixedLayer
from Script.assist.Array import Array
import Maps
import _thread
import time
import threading
import sys
class MCGame:
    _instance_lock = threading.Lock()
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600 , 600), 0, 32)
        pygame.display.set_mode((0,0),(pygame.DOUBLEBUF))   

        self.maps={}
    def LoadMap(self,map):
        self.map=map    
        self.map.LoadLevel()
        self.map.LoadMap(self.screen)
        self.player= MixedLayer.GetInstance().GetPlayer()
    def Update(self):
        game = 1
        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 接收到退出时间后退出程序
                    game = 0
                    break
    def Start(self):
        self.map.LoadMap(self.screen)
        #_thread.start_new_thread(self.forword,())
        self.Update()
    def forword(self):
        self.player.forword()
    def right(self):
        self.player.right()
    def left(self):
        self.player.left()
    def pickup(self):
        mixed = MixedLayer.GetInstance()
        for x in mixed.equList:
            self.player.CheckEqu()
            if x.equn == self.player.equn:
                mixed.equList.remove(x)
                del x
                print('Ok')
                break
                
        pass
    def __new__(cls, *args, **kwargs):
        if not hasattr(MCGame, "_instance"):
            with MCGame._instance_lock:
                if not hasattr(MCGame, "_instance"):
                    MCGame._instance = object.__new__(cls)  
        return MCGame._instance
    @staticmethod
    def GetInstance():
        return MCGame._instance