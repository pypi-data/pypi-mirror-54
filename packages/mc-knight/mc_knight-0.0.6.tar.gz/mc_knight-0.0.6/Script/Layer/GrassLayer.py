from Script.Layer.Layer import Layer
from Resources.sprites.grass.Grass import Grass
class GrassLyaer(Layer):
    def __init__(self,cols,rows):
        Layer.__init__(self,cols,rows)
        self.element=Grass()
        self.CreateLayer()
    def CreateLayer(self):
        for i in range(self.cols):
            for j in range(self.rows):
                self.myLayer[i,j]=self.element.GetElement()