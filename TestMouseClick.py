from ctypes import *
import win32api,win32gui,win32con
import time
for i in range(1,10):
    time.sleep(1)
    windll.user32.SetCursorPos(806, 522)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(1)
    windll.user32.SetCursorPos(1419, 330)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|win32con.MOUSEEVENTF_LEFTUP, 0, 0)