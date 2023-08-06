
from Script.mcgame.MCGameUnittest import *
import unittest

class myaction(unittest.TestCase):
    action=''
    @classmethod
    def setUpClass(self):
        self.action=unittest.TestSuite()
        print('开始输出操作队列：')
        
    def test_forword_run(self):
        self.action.addTest(mcgameunittest('test_forword_run'))

    def test_left_run(self):
        self.action.addTest(mcgameunittest('test_left_run'))

    def test_right_run(self):
        self.action.addTest(mcgameunittest('test_right_run'))

    def test_pickup_run(self):
        self.action.addTest(mcgameunittest('test_pickup_run'))
    def test_start_run(self):
        unittest.TextTestRunner().run(self.action)
    
class myscreen(unittest.TestCase):
    action=''
    @classmethod
    def setUpClass(self):
        self.action=unittest.TestSuite()
        print('开始屏幕刷新')
    def test_updateScreen_run(self):
        self.action.addTest(mcgameunittest('test_updateScreen_run'))

    def test_start_run(self):
        unittest.TextTestRunner().run(self.action)






