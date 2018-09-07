#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import win32gui, win32ui, win32con, win32api
from PIL import ImageGrab

hwnd = win32gui.FindWindow(None, '连连看外挂')
#返回(x1,y1,x2,y2)
p = win32gui.GetWindowRect(hwnd)
print(p)

im = ImageGrab.grab(p)
im.save('temp.jpg')