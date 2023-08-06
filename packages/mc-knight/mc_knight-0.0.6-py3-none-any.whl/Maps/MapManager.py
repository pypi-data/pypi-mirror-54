from Maps.Level01 import Level01
from Maps.Level02 import Level02
from Maps.Level03 import Level03
from Script.mcgame.MCGame import MCGame

def LoadLevel01():
    return Level01(MCGame.GetInstance().screen,3,3)
def LoadLevel02():
    return Level02(MCGame.GetInstance().screen,4,5)
def LoadLevel03():
    return Level03(MCGame.GetInstance().screen,7,8)
