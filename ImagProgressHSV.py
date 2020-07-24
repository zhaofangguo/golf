# coding=utf-8
"""
使用HSV方式处理图片，使用HSV阈值截断的方法进行判断，返回值为球的球心像素坐标
目标的下边长的中心坐标
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
    if flag == 'ball':  # 默认球为红色
        lowarray = np.array([0, 43, 46])
        higharray = np.array([120, 255, 255])  # 此处使用反向思维，直接允许红色之外的所有值通过，红色部分为黑色，在识别下摄像头时效果不错
    else:  # 默认洞为蓝色
        lowarray = np.array([100, 43, 46])
        higharray = np.array([124, 255, 255])  # 青色+蓝色
    # lowarraydark = np.array([0, 43, 46])
    # higharraydark = np.array([10, 255, 255])
    # 　二值化
    dst = cv.inRange(Image_HSV, lowarray, higharray)
    # dstdark = cv.inRange(Image_HSV, lowarraydark, higharraydark)
    # 中值滤波降噪，开运算降噪
    MedirImag = cv.medianBlur(dst, 9)
    element = cv.getStructuringElement(cv.MORPH_RECT, (13, 13))
    MedirImag = cv.morphologyEx(MedirImag, cv.MORPH_OPEN, element)
    result = cv.Canny(MedirImag, 50, 150)
    cv.imshow('canny', result)
    # MedirImagdark = cv.medianBlur(dstdark, 9)
    # element = cv.getStructuringElement(cv.MORPH_RECT, (13, 13))
    # MedirImagdark = cv.morphologyEx(MedirImagdark, cv.MORPH_OPEN, element)
    cv.imshow('testdark', MedirImag)
    # dark = cv.addWeighted(MedirImagdark, 0.5, MedirImag, 0.5, 0)
    # cv.imshow('add', dark)
    # 霍夫变换检测圆心cv.waitKey(0)
    if flag == 'ball':
        circles = cv.HoughCircles(result, cv.HOUGH_GRADIENT, 1, 60, param1=1, param2=5, minRadius=1, maxRadius=20)
        # 参数4是圆心距离，param2是v2.HOUGH_GRADIENT方法的累加器阈值。阈值越小，检测到的圈子越多。
        print circles
        for circle in circles[0]:
            x = int(circle[0])
            y = int(circle[1])
            r = int(circle[2])
            result = cv.circle(result, (x, y), r, (255, 255, 255), 1)
            result = cv.circle(result, (x, y), 2, (255, 255, 255), -1)
        data = [x, y]
    if flag == 'hole':
        x, y, w, h = cv.boundingRect(result)
        cv.rectangle(result, (x, y), (x + w, y + h), (255, 255, 255), 2)
        data = [x + w / 2, y + h ]
    print data
    cv.imshow('test', result)
    return data


if __name__ == "__main__":
    # robotIP = '169.254.202.17'
    # PORT = 9559
    # motionProxy = ALProxy("ALMotion", robotIP, PORT)
    # postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    # motionProxy.wakeUp()
    # postureProxy.goToPosture("StandInit", 0.5)
    # frame = getImag('169.254.202.17', 9559, 1, 'ahhhdvsrdhjgkjgi')
    frame = cv.imread('images/hole_afternoontop.jpg')
    ImagProgressHSV(frame, 'hole')
    cv.imshow('src', frame)
    # ImagProgressHSV(frame, 'hole')
    cv.waitKey(0)
    # print ImagProgress(frame, 1)
