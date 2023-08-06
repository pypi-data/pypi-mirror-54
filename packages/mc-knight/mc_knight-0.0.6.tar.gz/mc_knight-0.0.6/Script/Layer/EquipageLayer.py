from Script.Layer.Layer import Layer
from Script.equipage.equipage import equ
from Script.assist.Array import Array
class EquipageLayer(Layer):
    def __init__(self,cols,rows,array,blank,collider):
        Layer.__init__(self,cols,rows)
        self.array=array
        self.CreateLayer(blank,collider)
    def CreateLayer(self,blank,collider):
        for i in range(self.cols):
            for j in range(self.rows):
                if self.array[i,j]!=0:
                    if self.array[i,j]==1:
                        blank.equList.append(equ(self.array,'sword'))
                        self.array[i,j] = 0
                        collider[i,j]=3
                    elif self.array[i,j]==2:
                        blank.equList.append(equ(self.array,'shield'))
                        self.array[i,j] = 0
                        collider[i,j]=4
                    elif self.array[i,j]==3:
                        blank.equList.append(equ(self.array,'helmet'))
                        self.array[i,j] = 0
                        collider[i,j]=5


