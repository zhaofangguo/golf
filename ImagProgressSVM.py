# coding=utf-8
"""
使用SVM方式处理图片，加载训练xml文件，返回值为球的球心像素坐标
洞的球心像素坐标
"""
import cv2
from getImag import getImag
import numpy as np

robotIP = '169.254.202.17'
PORT = 9559


def ImagProgressSVM(img, flag):
    if flag == 'hole':
        svm_l = cv2.ml.SVM_load('svm_l.xml')
    else:
        pass
    image = img.copy()
    cv2.imshow("image", image)  # 摄像头采集到的原图, 其实可以不显示
    result = np.ones((image.shape[0], image.shape[1]), dtype=np.uint8)
    result[:, :] = 0
    for i in range(0, image.shape[0] - 1, 3):
        for j in range(0, image.shape[1] - 1, 3):
            point = image[i, j]
            sampleMat = np.vstack([point])
            sampleMat = np.array(sampleMat, dtype='float32')
            (c, response) = svm_l.predict(sampleMat)
            if response == 1:
                result[i, j] = 255
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("result", result)  # mask of interesting area
    circles = cv2.HoughCircles(result, cv2.HOUGH_GRADIENT, 1, 500, param1=1, param2=10, minRadius=100, maxRadius=500)
    # 参数4是圆心距离，param2是v2.HOUGH_GRADIENT方法的累加器阈值。阈值越小，检测到的圈子越多。
    print circles
    for circle in circles[0]:
        x = int(circle[0])
        y = int(circle[1])
        r = int(circle[2])
        img = cv2.circle(img, (x, y), r, (255, 255, 255), 1)
        img = cv2.circle(img, (x, y), 2, (255, 255, 255), -1)
    cv2.imshow('test', img)
    data = [x, y]
    # contours, hier = cv2.findContours(result, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # return result, image, contours
    return data


if __name__ == '__main__':
    image = cv2.imread('redballtest.jpg')
    ImagProgressSVM(image)
    cv2.waitKey(0)
