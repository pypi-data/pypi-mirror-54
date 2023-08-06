from Script.Layer.Layer import Layer
from Script.Player.Knight import Knight
from Script.assist.Array import Array
class PlayerLayer(Layer):
    def __init__(self,cols,rows,array):
        Layer.__init__(self,cols,rows)
        self.array=Array()
        self.array.Set(array)
        self.element = Knight(array)
        self.CreateLayer()
    def CreateLayer(self):
        pass

    def GetPlayer(self):
        return self.element.GetKnightAnim()
    def GetPlayerPos(self):
        return (self.element.x,self.element.y)