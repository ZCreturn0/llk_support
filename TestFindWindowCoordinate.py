from ctypes import *
import win32api,win32gui,win32con
import time
hwnd = win32gui.FindWindow(None, '计算器')
rect = win32gui.GetWindowRect(hwnd)
x = rect[0]
y = rect[1]
w = rect[2] - x
h = rect[3] - y
print("Window %s:" % (win32gui.GetWindowText(hwnd)))
print("Location: (%d, %d)" % (x, y))
print("Size: (%d, %d)" % (w, h))
time.sleep(1)
windll.user32.SetCursorPos((x+w-10), (y+10))
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|win32con.MOUSEEVENTF_LEFTUP, 0, 0)