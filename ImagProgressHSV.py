# coding=utf-8
"""
使用HSV方式处理图片，使用HSV阈值截断的方法进行判断，返回值为球的球心像素坐标
洞的球心像素坐标
"""
import cv2 as cv
import numpy as np
from getImag import getImag
from naoqi import ALProxy


def ImagProgressHSV(filename, flag):
    Image = filename
    # Image = cv.imread(filename)
    # 得到图片，搞高斯滤波+色彩转换
    cv.namedWindow('test', cv.WINDOW_NORMAL)
    Image_Gau = cv.GaussianBlur(Image, (9, 9), 0)
    Image_HSV = cv.cvtColor(Image_Gau, cv.COLOR_BGR2HSV)
    # HSV阈值设定
    if flag == 'ball':
        lowarray = np.array([140, 43, 46])
        higharray = np.array([180, 255, 255])
    else:
        lowarray = np.array([0, 43, 46])
        higharray = np.array([20, 255, 255])
    # lowarraydark = np.array([0, 43, 46])
    # higharraydark = np.array([10, 255, 255])
    # 　二值化
    dst = cv.inRange(Image_HSV, lowarray, higharray)
    # dstdark = cv.inRange(Image_HSV, lowarraydark, higharraydark)
    # 中值滤波降噪，开运算降噪
    MedirImag = cv.medianBlur(dst, 9)
    element = cv.getStructuringElement(cv.MORPH_RECT, (13, 13))
    MedirImag = cv.morphologyEx(MedirImag, cv.MORPH_OPEN, element)

    # MedirImagdark = cv.medianBlur(dstdark, 9)
    # element = cv.getStructuringElement(cv.MORPH_RECT, (13, 13))
    # MedirImagdark = cv.morphologyEx(MedirImagdark, cv.MORPH_OPEN, element)
    cv.imshow('testdark', MedirImag)
    # dark = cv.addWeighted(MedirImagdark, 0.5, MedirImag, 0.5, 0)
    # cv.imshow('add', dark)
    # 霍夫变换检测圆心
    cv.waitKey(0)
    circles = cv.HoughCircles(MedirImag, cv.HOUGH_GRADIENT, 1, 100, param1=1, param2=5, minRadius=1, maxRadius=1000)
    print circles
    if circles is None and flag == 'hole':
        return None
    cv.imshow('eter', MedirImag)
    for circle in circles[0]:
        # 圆的基本信息
        # print(circle[2])
        # 坐标行列
        x = int(circle[0])
        y = int(circle[1])
        # 半径
        r = int(circle[2])
        # 在原图用指定颜色标记出圆的位置
        # img = cv.circle(MedirImag, (x, y), r, (255, 255, 255), 3)
        # img = cv.circle(MedirImag, (x, y), 2, (255, 255, 255), -1)
        img = cv.circle(Image, (x, y), r, (255, 255, 255), 1)
        img = cv.circle(Image, (x, y), 2, (255, 255, 255), -1)
    cv.imshow('test', img)
    print x, y
    data = [x, y]
    return data


if __name__ == "__main__":
    robotIP = '169.254.202.17'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    frame = getImag('169.254.202.17', 9559, 1, 'ahhhfdvsrdhjgkjgi')
    ImagProgressHSV(frame, 'ball')
    # ImagProgressHSV(frame, 'hole')
    cv.waitKey(0)
    # print ImagProgress(frame, 1)
