from Maps.LevelBase import LevelBase
from Script.assist.Array import Array
class Level01(LevelBase):
    def __init__(self,screen,cols,rows):
        LevelBase.__init__(self,screen,cols,rows)
    def LoadLevel(self):
        array=Array(3,3)
        array[0,0] = 2
        array[0,1] = 2
        array[0,2] = 2
        array[2,0] = 1
        array[2,1] = 1
        array[2,2] = 1
        self.CreateWater(array)
        array.Clear()
        array[1,2] = 1
        self.CreateCastle(array)
        array.Clear()
        array[1,0]=1
        self.CreatePlayer(array)
        self.UpdateCollision()
        

