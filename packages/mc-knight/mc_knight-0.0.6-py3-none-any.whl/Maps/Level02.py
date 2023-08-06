from Maps.LevelBase import LevelBase
from Script.assist.Array import Array
class Level02(LevelBase):
    def __init__(self,screen,cols,rows):
        LevelBase.__init__(self,screen,cols,rows)
    def LoadLevel(self):
        array=Array(4,5)
        array[0,0] = 1
        array[0,1] = 1
        array[0,2] = 1
        array[0,3] = 1
        array[0,4] = 1
        array[1,0] = 1
        array[2,0] = 1
        array[3,2] = 1
        array[2,2] = 1
        array[1,4] = 1
        array[2,4] = 1
        array[3,4] = 1
        self.CreatePine(array)

        array.Clear()
        array[3,3] = 1
        self.CreateCastle(array)

        array.Clear()
        array[3,0] = 1
        self.CreatePlayer(array)
        self.UpdateCollision()

