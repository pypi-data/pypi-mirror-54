from Resources.sprites.Player.Player import Player
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
class KnightAnimation(Enum):
    #stay
    knight_stay='knight_stay'
    knight_stay_sword_shield='knight_stay_sword_shield'
    knight_stay_helmet_sword='knight_stay_helmet_sword'
    knight_stay_shield='knight_stay_shield'
    knight_stay_sword='knight_stay_sword'
    knight_stay_helmet='knight_stay_helmet'
    knight_stay_helmet_shield='knight_stay_helmet_shield'
    knight_stay_helmet_sword_shield='knight_stay_helmet_sword_shield'
    #walk
    knight_walk='knight_walk'
    knight_walk_shield='knight_walk_shield'
    knight_walk_helmet_shield='knight_walk_helmet_shield'
    knight_walk_helmet='knight_walk_helmet'
    knight_walk_sword='knight_walk_sword'
    knight_walk_helmet_sword='knight_walk_helmet_sword'
    knight_walk_sword_shield='knight_walk_sword_shield'
    knight_walk_helmet_sword_shield='knight_walk_helmet_sword_shield'
    #death
    knight_death='knight_death'
    knight_death_helmet_sword='knight_death_helmet_sword'
    knight_death_shield='knight_death_shield'
    knight_death_sword='knight_death_sword'
    knight_death_shield_sword='knight_death_shield_sword'
    knight_death_helmet_shield='knight_death_helmet_shield'
    knight_death_helmet_shield_sword='knight_death_helmet_shield_sword'
    
class Knight:
    _instance_lock = threading.Lock()
    def __init__(self,array,speed=1):
        self.speed=speed
        self.cols=array.cols
        self.rows=array.rows
        self.array=array
        self.direction=0
        temp=self.GetPos()
        self.x=temp[0]
        self.y=temp[1]
        self.posY=temp[3]
        self.posX=temp[2]
        self.player=Player()
        self.n=-1
        self.height=80
        self.width=60
        self.isWin=False
        self.isRot=False
        self.collider=Array(array.cols,array.rows)
        self.equn=0
        self.animn=0
        self.a=True
        self.b=True
        self.c=True
        self.KnightAnim=self.player.GetEement(KnightAnimation.knight_stay.value)
    def GetPos(self):
        for i in range(0,self.cols):  
             for j in range(self.rows):
                a=int(i*65+(300-(self.rows/2*65)))
                b=int(j*65+(300-(self.cols/2*65)))
                if self.array[j,i]:  
                    #print('abij:'+str((a,b,i,j)))
                    return (a,b,i,j)
    def SetCollision(self,array):
        self.collider.Set(array)
    def GetKnightAnim(self):
        if self.n<len(self.KnightAnim)-1:
            self.n+=1
        else:
            self.n=0
        if (1-self.isWin):
            if self.isRot:
                return pygame.transform.flip(self.KnightAnim[self.n],True,False)
            else:
                return self.KnightAnim[self.n]
        else:
            if self.height==0:
                os.system("pause")
            if self.width>35:
                self.width*=0.9
                self.height*=0.9
            else:
                self.width=self.height=0
                print('过关')
            if self.isRot:
                return pygame.transform.smoothscale(pygame.transform.flip(self.KnightAnim[self.n],True,False),(int(self.width),int(self.height)))
            else:
                return pygame.transform.smoothscale(self.KnightAnim[self.n],(int(self.width),int(self.height)))
            
    def __iter__(self):
        self.anim=-1
    def __next__(self):
        if self.anim<len(self.KnightAnim):
            self.anim=self.anim+1
            return self.KnightAnim[self.anim]
        else:
            return None
    def SetXY(self,x,y):
        self.x=x
        self.y=y
    def UpdateKnightAnimation(action):
        self.KnightAnim=self.player.GetEement(action)
    def CheckCollision(self):
        if self.direction==0 and self.CheckLevel((self.posY,self.posX+1)) and self.collider[self.posY,self.posX+1]==1:
            print('触发碰撞，类型1')
            return False
        elif self.direction==1 and self.CheckLevel((self.posY+1,self.posX)) and self.collider[self.posY+1,self.posX]==1:
            print('触发碰撞，类型1')
            return False
        elif self.direction==2 and self.CheckLevel((self.posY,self.posX-1)) and self.collider[self.posY,self.posX-1]==1: 
            print('触发碰撞，类型1')
            return False
        elif self.direction==3 and self.CheckLevel((self.posY-1,self.posX)) and self.collider[self.posY-1,self.posX]==1:
            print('触发碰撞，类型1')
            return False
        print('OK')
        return True
    def CheckLevel(self,pos):
        if self.collider[pos[0],pos[1]] == 2:
            print('触发碰撞，类型2')
            self.isWin=True
            #os.system("pause")
        return True
    def CheckEqu(self):
        if self.collider[(self.posX,self.posY)] == 3:
            if self.a:
                self.equn = 3
                self.animn+=1
                print('触发碰撞，类型3')
                self.a=False
        elif self.collider[(self.posX,self.posY)] == 4:
            if self.b:
                self.equn = 4
                self.animn+=3
                print('触发碰撞，类型3')
                self.b=False
        elif self.collider[(self.posX,self.posY)] == 5:
            if self.c:
                self.equn = 5
                self.animn+=5
                print('触发碰撞，类型3')
                self.c=False
        self.SwitchEqu(True)
    def SwitchEqu(self,b):
        if b:
            if self.animn == 0:
                self.KnightAnim=self.player.GetEement(KnightAnimation.knight_stay.value)
            elif self.animn == 1:
                self.KnightAnim=self.player.GetEement(KnightAnimation.knight_stay_sword.value)
            elif self.animn == 3:
                self.KnightAnim=self.player.GetEement(KnightAnimation.knight_stay_shield.value)
            elif self.animn == 5:
                self.KnightAnim=self.player.GetEement(KnightAnimation.knight_stay_helmet.value)
            elif self.animn == 4:
                self.KnightAnim=self.player.GetEement(KnightAnimation.knight_stay_sword_shield.value)
            elif self.animn == 8:
                self.KnightAnim=self.player.GetEement(KnightAnimation.knight_stay_helmet_shield.value)
            elif self.animn == 6:
                self.KnightAnim=self.player.GetEement(KnightAnimation.knight_stay_helmet_sword.value)
            elif self.animn == 9:
                self.KnightAnim=self.player.GetEement(KnightAnimation.knight_stay_helmet_sword_shield.value)
        else:
            if self.animn == 0:
                self.KnightAnim=self.player.GetEement(KnightAnimation.knight_walk.value)
            elif self.animn == 1:
                self.KnightAnim=self.player.GetEement(KnightAnimation.knight_walk_sword.value)
            elif self.animn == 3:
                self.KnightAnim=self.player.GetEement(KnightAnimation.knight_walk_shield.value)
            elif self.animn == 5:
                self.KnightAnim=self.player.GetEement(KnightAnimation.knight_walk_helmet.value)
            elif self.animn == 4:
                self.KnightAnim=self.player.GetEement(KnightAnimation.knight_walk_sword_shield.value)
            elif self.animn == 8:
                self.KnightAnim=self.player.GetEement(KnightAnimation.knight_walk_helmet_shield.value)
            elif self.animn == 6:
                self.KnightAnim=self.player.GetEement(KnightAnimation.knight_walk_helmet_sword.value)
            elif self.animn == 9:
                self.KnightAnim=self.player.GetEement(KnightAnimation.knight_walk_helmet_sword_shield.value)
    def forword(self):
        self.SwitchEqu(False)
        if self.direction==0:
            if self.posX+1 < self.rows and self.CheckCollision():
                self.posX+=1
                for i in range(65):
                    time.sleep(0.01)
                    self.x+=self.speed
        elif self.direction==1:
            if self.posY+1 < self.cols and self.CheckCollision():
                self.posY+=1
                for i in range(65):
                    time.sleep(0.01)
                    self.y+=self.speed
        elif self.direction==2:
            if self.posX-1 >= 0 and self.CheckCollision():
                self.posX-=1
                for i in range(65):
                    time.sleep(0.01)
                    self.x-=self.speed
        elif self.direction==3:
            if self.posY-1 >= 0 and self.CheckCollision():
                self.posY-=1
                for i in range(65):
                    time.sleep(0.01)
                    self.y-=self.speed
        self.SwitchEqu(True)
        return True
    def left(self):
        if (self.direction-1)<0:
            self.direction+=4
        self.direction-=1
        self.checkRAL()
        return True
    def right(self):
        if (self.direction+1)>3:
            self.direction-=4
        self.direction+=1
        self.checkRAL()
        return True
    def checkRAL(self):
        if self.direction==2:
            self.isRot=True
        elif self.direction==0:
            self.isRot=False
    @staticmethod
    def GetInstance():
        return Knight._instance
    def __new__(cls, *args, **kwargs):
        if not hasattr(Knight, "_instance"):
            with Knight._instance_lock:
                if not hasattr(Knight, "_instance"):
                    Knight._instance = object.__new__(cls)  
        return Knight._instance
