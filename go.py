#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import win32gui, win32ui, win32con, win32api
from PIL import ImageGrab,Image
import math,operator
from functools import reduce

class Point(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Tube(object):
    def __init__(self,s_point,e_point,value=0):
        self.s_point = s_point
        self.e_point = e_point
        self.value = value

hwnd = win32gui.FindWindow(None, 'QQ游戏 - 连连看角色版')  #QQ游戏 - 连连看角色版
#返回(x1,y1,x2,y2)
p = win32gui.GetWindowRect(hwnd)
print(p)

#游戏起始坐标
start_point = Point(14,181)
#方块宽高
tube_width = 31
tube_height = 35

#对游戏窗口进行截图
im = ImageGrab.grab(p)
im.save('temp.jpg')

#裁剪游戏区,把每个方块与空白区裁剪出来,游戏总共11行19列
for i in range(11):
    for j in range(19):
        #当前方块起始,结束坐标
        sp = Point(start_point.x+j*tube_width,start_point.y+tube_height*i)
        ep = Point(sp.x + tube_width,sp.y + tube_height)
        t = Tube(sp,ep)
        #裁剪
        cropedIm = im.crop((t.s_point.x,t.s_point.y,t.e_point.x,t.e_point.y))
        #保存为     "行数-列数.jpg"
        cropedIm.save('.\/cut\/%s-%s.jpg' % (i,j))