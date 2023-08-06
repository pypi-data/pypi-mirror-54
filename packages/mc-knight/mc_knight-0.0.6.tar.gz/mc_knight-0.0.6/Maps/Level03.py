from Maps.LevelBase import LevelBase
from Script.assist.Array import Array
class Level03(LevelBase):
    def __init__(self,screen,cols,rows):
        LevelBase.__init__(self,screen,cols,rows)
    def LoadLevel(self):
        array=Array(7,8)
        array[0,0] = 1
        array[0,1] = 1
        array[0,2] = 1
        array[0,3] = 1
        array[0,4] = 1
        array[0,5] = 1
        array[0,6] = 1
        array[0,7] = 1
        array[6,0] = 1
        array[6,1] = 1
        array[6,2] = 1
        array[6,3] = 1
        array[6,4] = 1
        array[6,5] = 1
        array[6,6] = 1
        array[6,7] = 1
        array[1,0] = 1
        array[2,0] = 1
        array[4,0] = 1
        array[5,0] = 1
        self.CreatePine(array)
        array.Clear()
        array[2,3] = 1
        array[3,3] = 1
        array[2,4] = 1
        array[3,4] = 1
        array[3,2] = 1
        self.CreateWater(array)
        array.Clear()
        array[2,2] = 1
        array[4,5] = 1
        array[2,5] = 1
        self.CreateStone(array)
        array.Clear()
        array[1,7]=1
        array[2,7]=1
        array[4,7]=1
        array[5,7]=1
        self.CreateStump(array)
        array.Clear()
        array[3,7] = 1
        self.CreateCastle(array)
        array.Clear()
        array[1,1] = 1
        self.CreateEquipage(array)
        array.Clear()
        array[6,5] = 2
        self.CreateEquipage(array)
        array.Clear()
        array[6,1] = 3
        self.CreateEquipage(array)
        array.Clear()
        array[3,0] = 1
        self.CreatePlayer(array)
        self.UpdateCollision()


