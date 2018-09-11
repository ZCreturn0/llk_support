#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import threading
import functools
import math,operator
import win32gui, win32ui, win32con, win32api

from functools import reduce
from datetime import datetime
from PIL import ImageGrab,Image
from multiprocessing import Process,Manager


#坐标点
class Point(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

#方块:起始坐标,终点坐标,点击坐标,列数,行数,值
class Tube(object):
    def __init__(self,s_point,e_point,m_point,x,y,value=0):
        self.s_point = s_point
        self.e_point = e_point
        self.click_point = m_point
        self.value = value
    def __str__(self):
        return 'start:%s,%s----end:%s,%s----click:%s,%s----(x,y):(%s,%s)----value:%s' % (self.s_point.x,self.s_point.y,self.e_point.x,self.e_point.y,self.click_point.x,self.click_point.y,self.x,self.y,self.value)

#值与图片配对,用于将游戏区转换为数组
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


#装饰器,打印执行时长
def log(text):
    def decoretor(func):
        @functools.wraps(func)
        def wrapper(*args,**kw):
            start = datetime.now()
            c = func(*args,**kw)
            print("%s ran in %s" % (func.__name__,datetime.now()-start))
            return c
        return wrapper
    return decoretor


#图片相似度begin

#primary  256*256
def make_regalur_image(img, size = (128, 128)):
	return img.resize(size).convert('RGB')

#primary  64*64
def split_image(img, part_size = (32, 32)):
	w, h = img.size
	pw, ph = part_size
#	assert w % pw == h % ph == 0
	return [img.crop((i, j, i+pw, j+ph)).copy() \
				for i in range(0, w, pw) \
				for j in range(0, h, ph)]

def hist_similar(lh, rh):
#	assert len(lh) == len(rh)
	return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)

def calc_similar(li, ri):
	return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0

#调用计算图片相似度,传入图片url
def calc_similar_by_path(lf, rf):
	li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
	return calc_similar(li, ri)

#调用计算图片相似度,传入图片对象
def calc_similar_by_obj(lf, rf):
	li, ri = make_regalur_image(lf), make_regalur_image(rf)
	return calc_similar(li, ri)

#传入img对象
def getValue(img):
    global imageValue,currentValue
    for item in imageValue:
        #相似度大于85%判定为同一张图片
        if calc_similar_by_obj(item.img,img) > 0.85:
            return item.val
    #未能在imageValue里找到对应图片,说明是一张新的图片,添加到imageValue里
    newImage = PictureValue(img,currentValue)
    currentValue += 1
    imageValue.append(newImage)
    return newImage.val

#差值感知算法
def dHash(img):
    #缩放8*8
    img=cv2.resize(img,(9,8),interpolation=cv2.INTER_CUBIC)
    #转换灰度图
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    hash_str=''
    #每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(8):
        for j in range(8):
            if   gray[i,j]>gray[i,j+1]:
                hash_str=hash_str+'1'
            else:
                hash_str=hash_str+'0'
    return hash_str

#Hash值对比
def cmpHash(hash1,hash2):
    n=0
    #hash长度不同则返回-1代表传参出错
    if len(hash1)!=len(hash2):
        return -1
    #遍历判断
    for i in range(len(hash1)):
        #不相等则n计数+1，n最终为相似度
        if hash1[i]!=hash2[i]:
            n=n+1
    return n
#图片相似度end

#获取中值坐标
def getMidPoint(p1,p2):
    x = (p1.x + p2.x) / 2
    y = (p1.y + p2.y) / 2
    return Point(x,y)

#是否在同一行
def inOneLine(t1,t2):
    return t1.x == t2.x

#是否在同一列
def inOneColumn(t1,t2):
    return t1.y == t2.y

#一行都为空[y1,y2)
def lineEmpty(m,y1,y2,x):
    empty = True
    for i in range(y1,y2):
        if m[x][i].value != 0:
            return False
    return empty

#一列都为空[x1,x2)
def columnEmpty(m,x1,x2,y):
    empty = True
    for i in range(x1,x2):
        if m[i][y].value != 0:
            return False
    return empty

#判断是否可消除;
#t1偏左上角,t2偏右下角
def canLink(m,x1,y1,x2,y2):
    t1 = m[x1][y1]
    t2 = m[x2][y2]
    if inOneLine(t1,t2) or inOneColumn(t1,t2):
        #相邻
        if(t2.x - t1.x == 1 or t2.y - t1.y == 1):
            return True
        else:
            #判断能否直连
            straight = True
            #计算中间格子是否都为空
            if inOneLine(t1,t2):
                straight = lineEmpty(m,y1,y2,x1)
            elif inOneColumn(t1,t2):
                straight = columnEmpty(m,x1,x2,y1)
            #中间格子都为空,能直连,返回True,否则继续
            if straight:
                return True
            else:
                if inOneLine(t1,t2):
                    cur = x1 - 1
                    while cur >= 0:
                        if columnEmpty(m,cur,x1,y1) and columnEmpty(m,cur,x2,y2) and lineEmpty(m,y1+1,y2,cur):
                            return True
                        elif not columnEmpty(m,cur,x1,y1) or not columnEmpty(m,cur,x2,y2):
                            break
                        cur -= 1
                    cur = x1 + 1
                    while cur <= 10:
                        if columnEmpty(m,x1+1,cur+1,y1) and columnEmpty(m,x2+1,cur+1,y2) and lineEmpty(m,y1+1,y2,cur):
                            return True
                        elif not columnEmpty(m,x1+1,cur+1,y1) or not columnEmpty(m,x2+1,cur+1,y2):
                            break
                        cur += 1
                elif inOneColumn(t1,t2):
                    cur = y1 - 1
                    while cur >= 0:
                        if lineEmpty(m,cur,y1,x1) and lineEmpty(m,cur,y2,x2) and columnEmpty(m,x1+1,x2,cur):
                            return True
                        elif not lineEmpty(m,cur,y1,x1) or not lineEmpty(m,cur,y2,x2):
                            break
                        cur -= 1
                    cur = x1 + 1
                    while cur <= 10:
                        if lineEmpty(m,y1+1,cur+1,x1) and lineEmpty(m,y2+1,cur+1,x2) and columnEmpty(m,x1+1,x2,cur):
                            return True
                        elif not lineEmpty(m,y1+1,cur+1,x1) or not lineEmpty(m,y2+1,cur+1,x2):
                            break
                        cur += 1
                return False



# hwnd = win32gui.FindWindow(None, 'QQ游戏 - 连连看角色版')  #QQ游戏 - 连连看角色版
# #返回(x1,y1,x2,y2)
# p = win32gui.GetWindowRect(hwnd)
# print(p)

#游戏起始坐标
start_point = Point(14,181)
#方块宽高
tube_width = 31
tube_height = 35

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




gameMap = []
start = datetime.now()


for i in range(11):
    values = []
    line = []
    for j in range(19):
        img = Image.open('./cut/%s-%s.jpg' % (i,j))
        value = getValue(img)
        values.append(value)
        print('%-2s' % (value),end="  ")
        #起始坐标
        s_px = start_point.x + j * tube_width;
        s_py = start_point.y + i * tube_height;
        #终止坐标
        e_px = (start_point.x + tube_width) + j * tube_width;
        e_py = (start_point.y + tube_height) + i * tube_height;
        s_point = Point(s_px,s_py)
        e_point = Point(e_px,e_py)
        tube = Tube(s_point,e_point,getMidPoint(s_point,e_point),i,j,value)
        # print(tube)
        line.append(tube)
    print('')
    gameMap.append(line)









print('Transform map in %s s' % (datetime.now() - start))


# def f(d,key,val):
#     d[key] = val
#     print(datetime.now())
#     print(d)

# if __name__ == '__main__':
#     with Manager() as manager:
#         d = manager.dict()
#         p_list = []
#         for i in range(10):
#             p = Process(target=f,args=(d,i,i))
#             p.start()
#             p_list.append(p)
#         for res in p_list:
#             res.join()

#         print(d)

#print(calc_similar_by_obj(Image.open('./cut/0-0.jpg'),Image.open('./bg/bg.jpg')))
