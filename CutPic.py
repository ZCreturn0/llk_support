#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
im = Image.open("temp.jpg")
'''
裁剪：传入一个元组作为参数
元组里的元素分别是：（距离图片左边界距离x， 距离图片上边界距离y，距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h）
'''
x = 358
y = 186
region = im.crop((x, y, 1027, 628))
region.save("./crop_test1.jpeg")
