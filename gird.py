# coding=utf-8
# 本py用于相机的标定和绘制棋盘格角点
from getImag import getImag
import cv2 as cv
import random
import numpy as np
import time


def gird(IP, PORT):
    criteria = (cv.TERM_CRITERIA_MAX_ITER | cv.TERM_CRITERIA_EPS, 30, 0.001)

    # 获取标定板角点的位置
    objp = np.zeros((6 * 9, 3), np.float32)
    objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)  # 将世界坐标系建在标定板上，所有点的Z坐标全部为0，所以只需要赋值x和y

    obj_points = []  # 存储3D点
    img_points = []  # 存储2D点
    images = []
    for i in range(0, 11):
        name = str(random.randint(1, 1000))
        images.append(getImag(IP, PORT, 1, name))
        print 'continue'
        time.sleep(2)
    for frame in images:
        img = frame
        cv.imshow('img', img)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        size = gray.shape[::-1]
        ret, corners = cv.findChessboardCorners(gray, (6, 9), None)
        print(ret)

        if ret:

            obj_points.append(objp)

            corners2 = cv.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)  # 在原角点的基础上寻找亚像素角点
            # print(corners2)
            if [corners2]:
                img_points.append(corners2)
            else:
                img_points.append(corners)

            cv.drawChessboardCorners(img, (8, 6), corners, ret)  # 记住，OpenCV的绘制函数一般无返回值
            cv.imshow('img', img)
            name = str(random.randint(1, 1000))
            name = name + '.jpg'
            cv.imwrite(name, img)
            cv.waitKey(5000)

    print(len(img_points))
    cv.destroyAllWindows()

    # 标定
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(obj_points, img_points, size, None, None)

    print("ret:", ret)
    print("mtx:\n", mtx)  # 内参数矩阵
    print("dist:\n", dist)  # 畸变系数   distortion cofficients = (k_1,k_2,p_1,p_2,k_3)
    print("rvecs:\n", rvecs)  # 旋转向量  # 外参数
    print("tvecs:\n", tvecs)  # 平移向量  # 外参数
    print("-----------------------------------------------------")
    cv.waitKey(0)


if __name__ == '__main__':
    IP = '169.254.202.17'
    PORT = 9559
    gird(IP, PORT)
