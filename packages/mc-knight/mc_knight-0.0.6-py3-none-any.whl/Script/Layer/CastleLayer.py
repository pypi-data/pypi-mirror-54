from Script.Layer.Layer import Layer
from Resources.sprites.castle.Castle01 import Castle
from Script.assist.Array import Array
class CastleLayer(Layer):
    def __init__(self,cols,rows,array,blank,collider):
        Layer.__init__(self,cols,rows)
        self.array=Array()
        self.array.Set(array)
        self.element=Castle()
        self.CreateLayer(blank,collider)
    def CreateLayer(self,blank,collider):
        for i in range(self.cols):
            for j in range(self.rows):
                if self.array[i,j]!=0:
                    collider[i,j]=2
                    blank.myLayer[i,j]=self.element.GetElement()


