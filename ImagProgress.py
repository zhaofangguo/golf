# coding=utf-8
import cv2 as cv
import numpy as np
from getImag import getImag


# 本py为图像处理部分,golf项目应该返回球的圆心坐标
def ImagProgress(filename):
    Image = filename
    # Image = cv.imread(filename)
    cv.namedWindow('test', cv.WINDOW_NORMAL)
    Image_Gau = cv.GaussianBlur(Image, (9, 9), 0)
    Image_HSV = cv.cvtColor(Image_Gau, cv.COLOR_BGR2HSV)
    # red limitition
    lowarray = np.array([0, 43, 46])
    higharray = np.array([20, 255, 255])
    # lowarraydark = np.array([0, 43, 46])
    # higharraydark = np.array([10, 255, 255])
    dst = cv.inRange(Image_HSV, lowarray, higharray)
    # dstdark = cv.inRange(Image_HSV, lowarraydark, higharraydark)
    MedirImag = cv.medianBlur(dst, 9)
    element = cv.getStructuringElement(cv.MORPH_RECT, (13, 13))
    MedirImag = cv.morphologyEx(MedirImag, cv.MORPH_OPEN, element)

    # MedirImagdark = cv.medianBlur(dstdark, 9)
    # element = cv.getStructuringElement(cv.MORPH_RECT, (13, 13))
    # MedirImagdark = cv.morphologyEx(MedirImagdark, cv.MORPH_OPEN, element)
    # cv.imshow('testdark', MedirImagdark)
    # dark = cv.addWeighted(MedirImagdark, 0.5, MedirImag, 0.5, 0)
    # cv.imshow('add', dark)
    circles = cv.HoughCircles(MedirImag, cv.HOUGH_GRADIENT, 1, 100, param1=1, param2=5, minRadius=1, maxRadius=1000)
    print circles
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
    # cv.waitKey(0)
    data = [x, y]
    return data


if __name__ == "__main__":
    frame = getImag('169.254.202.17', 9559, 1, 'ahhjgkjgi')
    ImagProgress(frame)
    # print ImagProgress(frame, 1)
