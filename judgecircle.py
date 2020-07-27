# -*- encoding: utf-8 -*-
"""
@File    :   judgecircle.py    

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/27 下午8:45 

@Author :   赵方国        
"""
import cv2 as cv
import numpy as np


def judgecircle(frame, data):
    """
    该函数将计算roi区域中的红绿颜色比，若在0.7和0.9之间，则返回真值，借此判断是否霍夫变换求得是真的球

    :param frame: 一张彩色源图
    :param data: 霍夫变换求得的数组，为【圆心x坐标，圆心y坐标，圆半径】
    :return: 当判断为真实红球时，返回真值
    """
    x = int(data[0])
    y = int(data[1])
    r = int(data[2])
    a = int(y - 2 * r)
    b = int(y + 2 * r)
    c = int(x - 2 * r)
    d = int(x + 2 * r)
    roi = frame[a:b, c:d]
    roihsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
    lowarraygreen = np.array([30, 43, 46])
    higharraygreen = np.array([80, 255, 255])
    roi = cv.inRange(roihsv, lowarraygreen, higharraygreen)
    count = 0
    for row in range(2 * r):
        for col in range(2 * r):
            pv = roi[row, col]
            if pv == 0:
                count += 1
    flag = float(count) / float(16 * r * r)
    if 0.2 < flag < 0.3:
        return True
    else:
        return False
