from Script.assist.Array import Array
from Script.Layer.Layer import Layer
class BlankLayer(Layer):
    def __init__(self,cols,rows):
        Layer.__init__(self,cols,rows)
        self.element=Array(cols,rows)

