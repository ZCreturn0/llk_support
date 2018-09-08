#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import win32gui, win32ui, win32con, win32api
from PIL import ImageGrab

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

start_point = Point(14,181)
tube_width = 31
tube_height = 35

im = ImageGrab.grab(p)
im.save('temp.jpg')

# cropedIm = im.crop((100,100,200,200))
# cropedIm.save('1-1.jpg')

for i in range(11):
    for j in range(19):
        sp = Point(start_point.x+j*tube_width,start_point.y+tube_height*i)
        ep = Point(sp.x + tube_width,sp.y + tube_height)
        t = Tube(sp,ep)
        cropedIm = im.crop((t.s_point.x,t.s_point.y,t.e_point.x,t.e_point.y))
        cropedIm.save('.\/cut\/%s-%s.jpg' % (i,j))