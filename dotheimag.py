# -*- encoding: UTF-8 -*-
"""
从准备状态的NAO摄像头获取不同场景下的图片,并拼接成一张,方便训练和识别
"""

import cv2
import numpy as np
import random
from naoqi import ALProxy
from PIL import Image
import os
import math

IMAGE_SIZE_W = 320  # 每张小图片的宽
IMAGE_SIZE_H = 240  # 每张小图片的高

IMAGE_ROW = 2  # 图片间隔，也就是合并成一张图后，一共有几行
IMAGE_COLUMN = 2  # 图片间隔，也就是合并成一张图后，一共有几列

# 获取图片集地址下的所有图片名称
image_names = ['morning.jpg', 'morning2.jpg', 'morninginit.jpg', 'morninginit2.jpg']

# 简单的对于参数的设定和实际图片集的大小进行数量判断
print len(image_names)
if len(image_names) != IMAGE_ROW * IMAGE_COLUMN:
    raise ValueError("合成图片的参数和要求的数量不能匹配！")

# 定义图像拼接函数
to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE_W, IMAGE_ROW * IMAGE_SIZE_H))  # 创建一个新图

# 循环遍历，把每张图片按顺序粘贴到对应位置上
for y in range(1, IMAGE_ROW + 1):
    for x in range(1, IMAGE_COLUMN + 1):
        from_image = Image.open(image_names[IMAGE_COLUMN * (y - 1) + x - 1]).resize(
            (IMAGE_SIZE_W, IMAGE_SIZE_H), Image.ANTIALIAS)  # 重塑（统一）照片的大小
        to_image.paste(from_image, ((x - 1) * IMAGE_SIZE_W, (y - 1) * IMAGE_SIZE_H))
        # im.paste(image, position)---粘贴image到im的position（左上角）位置。

to_image.save('final.jpg')  # 保存新图

print 'work done'
