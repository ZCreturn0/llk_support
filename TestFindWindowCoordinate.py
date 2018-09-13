import win32gui 
hwnd = win32gui.FindWindow(None, '计算器')
rect = win32gui.GetWindowRect(hwnd)
x = rect[0]
y = rect[1]
w = rect[2] - x
h = rect[3] - y
print("Window %s:" % (win32gui.GetWindowText(hwnd)))
print("Location: (%d, %d)" % (x, y))
print("Size: (%d, %d)" % (w, h))