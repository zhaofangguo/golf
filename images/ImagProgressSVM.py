# coding=utf-8
"""
使用SVM方式处理图片，加载训练xml文件，返回值为球的球心像素坐标
洞的球心像素坐标
会有过拟合的情况，在选点的时候不能选多，或者可以对决策树进行剪枝
"""
import cv2
from getImag import getImag
from naoqi import ALProxy
import numpy as np

robotIP = '169.254.202.17'
PORT = 9559


def ImagProgressSVM(img, flag):
    if flag == 'ball':
        svm_l = cv2.ml.SVM_load('svm_ball_morining.xml')
    else:
        svm_l = cv2.ml.SVM_load('svm_hole.xml')
    image = img.copy()
    cv2.imshow("image", image)  # 摄像头采集到的原图, 其实可以不显示
    result = np.ones((image.shape[0], image.shape[1]), dtype=np.uint8)
    result[:, :] = 0  # 此处将整张图置为黑色
    for i in range(0, image.shape[0] - 1, 3):
        for j in range(0, image.shape[1] - 1, 3):
            point = image[i, j]
            sampleMat = np.vstack([point])
            sampleMat = np.array(sampleMat, dtype='float32')
            (c, response) = svm_l.predict(sampleMat)
            # predict实现分类
            if response == 1:  # 满足分类条件的点置为白色
                result[i, j] = 255
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("result", result)  # mask of interesting area
    result = cv2.Canny(result, 50, 150)
    cv2.imshow('canny', result)
    # cv2.waitKey(0)
    if flag == 'ball':
        circles = cv2.HoughCircles(result, cv2.HOUGH_GRADIENT, 1, 60, param1=1, param2=5, minRadius=1, maxRadius=20)
        # 参数4是圆心距离，param2是v2.HOUGH_GRADIENT方法的累加器阈值。阈值越小，检测到的圈子越多。
        print circles
        for circle in circles[0]:
            x = int(circle[0])
            y = int(circle[1])
            r = int(circle[2])
            img = cv2.circle(img, (x, y), r, (255, 255, 255), 1)
            img = cv2.circle(img, (x, y), 2, (255, 255, 255), -1)
        data = [x, y]
    if flag == 'hole':
        x, y, w, h = cv2.boundingRect(result)
        cv2.rectangle(result, (x, y), (x + w, y + h), (255, 255, 255), 2)
        data = [x + w / 2, y + h / 2]
    cv2.imshow('test', result)
    print data
    # 此处为获得白色面积的像素数，使用双重遍历方式进行存储，为最终无奈之举，一旦使用，需要替换距离获取函数部分
    # 和其余所有使用霍夫变换圆心和外接矩形的部分
    # height = result.shape[0]
    # weight = result.shape[1]
    # count = 0
    # countdark = 0
    # for row in range(height):
    #     for col in range(weight):
    #         pv = result[row, col]
    #         # print pv
    #         if pv == 255:
    #             count += 1
    # print count + countdark
    # contours, hier = cv2.findContours(result, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # return result, image, contours
    return data


if __name__ == '__main__':
    image = cv2.imread('hole_afternoontop3.jpg')
    # motionProxy = ALProxy("ALMotion", robotIP, PORT)
    # postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    # motionProxy.wakeUp()
    # postureProxy.goToPosture("StandInit", 0.5)
    # image = getImag('169.254.202.17', 9559, 1, 'aeogkhscaagihaf')
    # cv2.imwrite('morninginit2.jpg', image)
    ImagProgressSVM(image, 'hole')
    cv2.waitKey(0)
