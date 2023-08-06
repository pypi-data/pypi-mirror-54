from Script.Layer.Layer import Layer
from Resources.sprites.background.BackGround import BackGround
from Script.assist.Array import Array
class BackGroundLayer(Layer):
    def __init__(self):
        Layer.__init__(self,0,0)
        self.element=BackGround()
    def GetBackGround(self):
        return self.element.GetEement()

