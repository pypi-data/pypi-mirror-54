from Resources.sprites.equipage.equipage import equipage
from Script.assist.Array import Array
from Script.Layer.MixedLayer import *
import os
import pygame
from pygame.locals import *
import Script.assist.ThreadPool
import time
import _thread
import threading
from enum import Enum
class EquipageAnimation(Enum):
    wolf = 'wolf'
    shield = 'shield'
    helmet = 'helmet'
    sword = 'sword'
    boom = 'boom'
class equ:
    def __init__(self,array,str):
        self.cols=array.cols
        self.rows=array.rows
        self.array=array
        self.n=-1
        temp=self.GetPos()
        self.x=temp[0]
        self.y=temp[1]
        self.posY=temp[3]
        self.posX=temp[2]
        self.equn=0
        self.e=equipage()
        if str == 'sword':
            self.equAnim=self.e.GetEement(EquipageAnimation.sword.value)
            self.equn=3
        elif str == 'shield':
            self.equAnim=self.e.GetEement(EquipageAnimation.shield.value)
            self.equn=4
        elif str == 'helmet':
            self.equAnim=self.e.GetEement(EquipageAnimation.helmet.value)
            self.equn=5
        pass
    def GetPos(self):
        for i in range(0,self.cols):  
             for j in range(self.rows):
                a=int(i*65+(300-(self.rows/2*65)))
                b=int(j*65+(300-(self.cols/2*65))+20)
                if self.array[i,j]:
                    print(self.array[i,j])
                    #print('abij:'+str((a,b,i,j)))
                    return (a,b,i,j)
    def GetAnim(self):
        if self.n<len(self.equAnim)-1:
            self.n+=1
        else:
            self.n=0
        return self.equAnim[self.n]
    def __iter__(self):
        self.anim=-1
    def __next__(self):
        if self.anim<len(self.KnightAnim):
            self.anim=self.anim+1
            return self.equAnim[self.anim]
        else:
            return None


