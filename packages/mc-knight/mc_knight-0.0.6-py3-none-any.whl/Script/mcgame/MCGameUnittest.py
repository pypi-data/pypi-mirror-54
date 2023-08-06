from Script.mcgame.MCGame import MCGame
import _thread
import unittest
import time
import Maps.MapManager

mygame=MCGame()

def SetMapName(name):
    mygame.LoadMap(name)

class mcgameunittest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass
        #mygame.LoadMap(Maps.MapManager.LoadLevel01())
    def test_forword_run(self):
        mygame.forword()

    def test_left_run(self):
        mygame.left()

    def test_right_run(self):
        mygame.right()
        
    def test_updateScreen_run(self):
        mygame.Update()

    def test_pickup_run(self):
        mygame.pickup()

