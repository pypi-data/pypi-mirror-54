
from Script.mcgame.MCUnittest import *
import Script.mcgame.MCGameUnittest as mc
import Maps.MapManager
import _thread
import time
from enum import Enum
print('欢迎使用魔扣少儿编程')
print('您可以尝试输入  MCPython.help()获取帮助信息！')
#print('此版本还未添加打包序列')
print('----------------------------------------------------------------')

def help():
    print('输入  MCPython.LoadMap(关卡)来加载关卡')
    print('例如  MCPython.LoadMap(1)来加载关卡')
    print('')
    print('加载关卡请放在最前面，不然骑士无法知道怎么移动')
    print('')
    print('输入  MCPython.moveFoward()来控制人物移动')
    print('输入  MCPython.turnLeft()来控制人物左转')
    print('输入  MCPython.turnRight()来控制人物右转')
    print('输入  MCPython.pickUp()来控制人物进行操作')
    print('')
    print('输入  MCPython.start()来开始游戏，请务必放在最后')
    print('----------------------------------------------------------------')


action = unittest.TestSuite()
updatescreen=unittest.TestSuite()

def chooseMap(id):
    temp = None
    if id == 1:
        temp = Maps.MapManager.LoadLevel01()
    elif id == 2:
        temp = Maps.MapManager.LoadLevel02()
    elif id == 3:
        temp = Maps.MapManager.LoadLevel03()
    mc.SetMapName(temp)
def actionimplement():
    time.sleep(1)
    unittest.TextTestRunner().run(action)

def moveFoward():
    action.addTest(myaction('test_forword_run'))
    print('forword')

def pickUp():
    action.addTest(myaction('test_pickup_run'))
    print('pickUp')

def turnLeft():
    action.addTest(myaction('test_left_run'))
    print('left')

def turnRight():
    action.addTest(myaction('test_right_run'))
    print('right')
def start(): 
    action.addTest(myaction('test_start_run'))
    updatescreen.addTest(myscreen('test_updateScreen_run'))
    updatescreen.addTest(myscreen('test_start_run'))
    _thread.start_new_thread(actionimplement,())
    unittest.TextTestRunner().run(updatescreen)