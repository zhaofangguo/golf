# -*- encoding: utf-8 -*-
"""
@File    :   ImagProgressHSV.py

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/25 下午10:16

@Author :   赵方国
"""
import random

import cv2 as cv
import numpy as np

from getImagfromvedio import getImagfromvedio
from naoqi import ALProxy


def ImagProgressHSV(filename, flag, flag2):
    """
    处理图片，进行阈值化。

    :param filename: 图片一张，由getImag函数获得
    :param flag: “ball”为处理球，进行霍夫圆变换，“hole”为处理球门，生成外接矩形
    :param flag2: 0为上摄像头传回来的图片，1为下摄像头传回来的图片
    :return: 两个元素的数组，球返回球心的x，y坐标。球洞返回矩形的下边中心x，y坐标,frame黑白图一张，供遍历像素函数使用
    """

    Image = filename
    # Image = cv.imread(filename)
    # 得到图片，搞高斯滤波+色彩转换
    # cv.namedWindow('test', cv.WINDOW_NORMAL)
    Image_Gau = cv.GaussianBlur(Image, (9, 9), 0)
    Image_HSV = cv.cvtColor(Image_Gau, cv.COLOR_BGR2HSV)
    # print Image_HSV[180, 180]
    # HSV阈值设定
    lowarrayball = np.array([150, 43, 46])
    higharrayball = np.array([180, 255, 255])  # 此处使用反向思维，直接允许红色之外的所有值通过，红色部分为黑色，在识别下摄像头时效果不错

    lowarrayhole = np.array([100, 43, 46])
    higharrayhole = np.array([124, 255, 255])  # 青色+蓝色
    # lowarraydark = np.array([0, 43, 46])
    # higharraydark = np.array([10, 255, 255])
    # 　二值化
    dstball = cv.inRange(Image_HSV, lowarrayball, higharrayball)
    dsthole = cv.inRange(Image_HSV, lowarrayhole, higharrayhole)
    # dstdark = cv.inRange(Image_HSV, lowarraydark, higharraydark)
    # 中值滤波降噪，开运算降噪
    MedirImagball = cv.medianBlur(dstball, 3)
    MedirImaghole = cv.medianBlur(dsthole, 3)
    element = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    MedirImagball = cv.morphologyEx(MedirImagball, cv.MORPH_OPEN, element)
    MedirImaghole = cv.morphologyEx(MedirImaghole, cv.MORPH_OPEN, element)
    cv.imshow('mediaball', MedirImagball)
    cv.imshow('mediahole', MedirImaghole)
    resultball = cv.Canny(MedirImagball, 50, 150)
    resulthole = cv.Canny(MedirImaghole, 50, 150)
    # cv.imshow('canny', result)
    # MedirImagdark = cv.medianBlur(dstdark, 9)
    # element = cv.getStructuringElement(cv.MORPH_RECT, (13, 13))
    # MedirImagdark = cv.morphologyEx(MedirImagdark, cv.MORPH_OPEN, element)
    # cv.imshow('testdark', MedirImag)
    # dark = cv.addWeighted(MedirImagdark, 0.5, MedirImag, 0.5, 0)
    # cv.imshow('add', dark)
    # 霍夫变换检测圆心cv.waitKey(0)
    # if flag == 'ball':
    #     circles = cv.HoughCircles(result, cv.HOUGH_GRADIENT, 1, 60, param1=1, param2=5, minRadius=1, maxRadius=20)
    #     # 参数4是圆心距离，param2是v2.HOUGH_GRADIENT方法的累加器阈值。阈值越小，检测到的圈子越多。
    #     # print circles
    #     i = 0
    #     for ci in circles[0]:
    #         i += 1
    #     if i != 1:
    #         for circle in circles[0]:
    #             if judgecircle(Image, circle):
    #                 circleflag = circle
    #     else:
    #         circleflag = circles[0]
    #     print circleflag
    #     x = int(circleflag[0][0])
    #     y = int(circleflag[0][1])
    #     r = int(circleflag[0][2])
    #     result = cv.circle(result, (x, y), r, (255, 255, 255), 1)
    #     result = cv.circle(result, (x, y), 2, (255, 255, 255), -1)
    #     data = [x, y]
    # if flag == 'hole':
    #     x, y, w, h = cv.boundingRect(result)
    #     cv.rectangle(result, (x, y), (x + w, y + h), (255, 255, 255), 2)
    #     data = [x + w / 2, y + h]
    # # print data
    # cv.imshow('test', result)
    # TODO 此处的try希望能够在没有检测到园的时候不让程序崩溃，并且希望能返回一个值用于目标是否存在的检测
    try:
        circles = cv.HoughCircles(resultball, cv.HOUGH_GRADIENT, 1, 60, param1=1, param2=5, minRadius=10, maxRadius=50)
        # 参数4是圆心距离，param2是v2.HOUGH_GRADIENT方法的累加器阈值。阈值越小，检测到的圈子越多。
        # print circles
        for circle in circles[0]:
            x = int(circle[0])
            y = int(circle[1])
            r = int(circle[2])
            Imag1 = cv.circle(Image, (x, y), r, (0, 255, 0), 1)
            result = cv.circle(Imag1, (x, y), 2, (0, 255, 0), -1)
        databall = [x, y]
    except TypeError:
        print 'NULL NULL NULL NULL NULL NULL NULL'
    try:
        x, y, w, h = cv.boundingRect(resulthole)
        cv.rectangle(Image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        result = Image
        datahole = [x + w / 2, y + h]
    except TypeError:
        print 'NULL NULL NULL NULL NULL NULL NULL'
    # print data
    cv.imshow('test', result)
    try:
        data = [databall, datahole]
        return data, MedirImagball
    except UnboundLocalError:
        print 'NULL NULL NULL NULL NULL NULL NULL'
        return [[0, 0], [0, 0]], MedirImagball


if __name__ == "__main__":
    robotIP = '169.254.252.60'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    name = str(random.randint(1, 1000))
    while True:
        try:
            print ImagProgressHSV(getImagfromvedio(robotIP, 9559, 1), 'ball', 1)[0][0]
        except TypeError:
            print 'wrong'
        cv.waitKey(1)
