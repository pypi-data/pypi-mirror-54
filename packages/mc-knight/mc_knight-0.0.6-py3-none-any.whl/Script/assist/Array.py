import copy
class Array:
    def __init__(self,cols=0,rows=0):
        self.cols=cols
        self.rows=rows
        self.array=[[0]*self.rows for i in range(self.cols)]
    def Set(self,array):
        self.array=array.array
    def Set2(self,array):
        self.array=array
    def Get(self):
        return self.array
    def Clear(self):
        self.array.clear()
        self.array=[[0]*self.rows for i in range(self.cols)]
    def __setitem__(self, key, value): 
        self.array[key[0]][key[1]]=value
    def __getitem__(self, key):
        return self.array[key[0]][key[1]]
    def __delitem__(self, key):
        del self.array[key[0]][key[1]]
    def __len__(self,index):
        if index==0:
            return self.cols
        elif index==1:
            return self.rows
    def __call__(self):
        return self

