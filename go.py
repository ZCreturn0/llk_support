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

class PictureValue(object):
    def __init__(self,img,val):
        self.img = img
        self.val = val

#存储所有图片的value,存PictureValue
imageValue = []
currentValue = 0
#把背景添加进去
bg = PictureValue(Image.open('./bg/bg.jpg'),currentValue)
currentValue += 1
imageValue.append(bg)

#图片相似度begin
def make_regalur_image(img, size = (256, 256)):
	return img.resize(size).convert('RGB')

def split_image(img, part_size = (64, 64)):
	w, h = img.size
	pw, ph = part_size
	assert w % pw == h % ph == 0
	return [img.crop((i, j, i+pw, j+ph)).copy() \
				for i in range(0, w, pw) \
				for j in range(0, h, ph)]

def hist_similar(lh, rh):
	assert len(lh) == len(rh)
	return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)

#调用计算图片相似度,传入图片对象
def calc_similar(li, ri):
	return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0

#调用计算图片相似度,传入图片url
def calc_similar_by_path(lf, rf):
	li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
	return calc_similar(li, ri)

#传入img对象
def getValue(img):
    global imageValue,currentValue
    for item in imageValue:
        #相似度大于85%判定为同一张图片
        if calc_similar(item.img,img) > 0.85:
            return item.img.val
    #未能在imageValue里找到对应图片,说明是一张新的图片,添加到imageValue里
    newImage = PictureValue(img,currentValue)
    currentValue += 1
    imageValue.append(newImage)
    return newImage.val
#图片相似度end



# hwnd = win32gui.FindWindow(None, 'QQ游戏 - 连连看角色版')  #QQ游戏 - 连连看角色版
# #返回(x1,y1,x2,y2)
# p = win32gui.GetWindowRect(hwnd)
# print(p)

# #游戏起始坐标
# start_point = Point(14,181)
# #方块宽高
# tube_width = 31
# tube_height = 35

# #对游戏窗口进行截图
# im = ImageGrab.grab(p)
# im.save('temp.jpg')

# #裁剪游戏区,把每个方块与空白区裁剪出来,游戏总共11行19列
# for i in range(11):
#     for j in range(19):
#         #当前方块起始,结束坐标
#         sp = Point(start_point.x+j*tube_width,start_point.y+tube_height*i)
#         ep = Point(sp.x + tube_width,sp.y + tube_height)
#         t = Tube(sp,ep)
#         #裁剪
#         cropedIm = im.crop((t.s_point.x,t.s_point.y,t.e_point.x,t.e_point.y))
#         #保存为     "行数-列数.jpg"
#         cropedIm.save('.\/cut\/%s-%s.jpg' % (i,j))

# img1 = Image.open('./cut/0-8.jpg')
# img2 = Image.open('./cut/0-11.jpg')