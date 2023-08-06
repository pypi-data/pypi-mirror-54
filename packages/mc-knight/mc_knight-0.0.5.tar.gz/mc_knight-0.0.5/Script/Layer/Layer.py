from Script.assist.Array import Array
class Layer:
    def __init__(self,cols,rows):
        self.cols=cols
        self.rows=rows
        self.element=None
        self.array=Array(cols,rows)
        self.myLayer=self.array()
    def GetLayer(self):
        return self.myLayer
    def CreateLayer(self):
        pass