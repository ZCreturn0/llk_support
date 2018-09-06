#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2

#打开图片
# img = cv2.imread('./origin.jpg')
# cv2.namedWindow('img')
# cv2.imshow('img',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

img1 = cv2.imread('./origin.jpg')
img2 = cv2.imread('./originCopy.jpg')

test1 = cv2.imread('./test1.jpg')
test2 = cv2.imread('./test2.jpg')
test3 = cv2.imread('./test3.jpg')

cut = cv2.imread('./cut.jpg')

#均值哈希算法
def aHash(img):
    #缩放为20*20
    img=cv2.resize(img,(20,20),interpolation=cv2.INTER_CUBIC)
    #转换为灰度图
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #s为像素和初值为0，hash_str为hash值初值为''
    s=0
    hash_str=''
    #遍历累加求像素和
    for i in range(20):
        for j in range(20):
            s=s+gray[i,j]
    #求平均灰度
    avg=s/400
    #灰度大于平均值为1相反为0生成图片的hash值
    for i in range(20):
        for j in range(20):
            if  gray[i,j]>avg:
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

print(aHash(img1))
print(aHash(img2))

print(aHash(test1))
print(aHash(test2))
print(aHash(test3))

print(aHash(cut))

print(cmpHash(aHash(img1),aHash(img2)))
print(cmpHash(aHash(img1),aHash(cut)))
print(cmpHash(aHash(img1),aHash(test1)))