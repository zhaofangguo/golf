# -*- encoding: UTF-8 -*-
"""
从获取的拼接成一张的图片,进行训练和识别
但容易过拟合
是训练SVM的脚本，生成的xml文件会被别的脚本调用
应该生成两个xml，一个是球的，一个是洞的
"""

import cv2
import numpy as np
import time

global label
label = [[0]]
global targetImage
targetImage = [[0, 0, 0]]


def main(imag):
    global image
    image = imag
    cv2.namedWindow("wdname", 0)
    cv2.setMouseCallback("wdname", on_EVENT_LBUTTONDOWN)
    cv2.imshow("wdname", image)
    global flag
    global ffflag
    ffflag = False
    flag = 1
    while True:
        c = cv2.waitKey(0)
        if (c & 255) == 27:
            cv2.destroyAllWindows()
            print "Exiting ..."
            break
        if chr(c) == 'q':
            flag = 0
        # if chr(c) == 'q':
        #
        #     break
    SVM()


def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    global ffflag
    if event == cv2.EVENT_LBUTTONDOWN:
        ffflag = True
    elif event == cv2.EVENT_LBUTTONUP:
        ffflag = False
    if ffflag:
        global image
        Point = image[y, x]
        tmp = [Point[0], Point[1], Point[2]]
        global targetImage
        targetImage = np.vstack((targetImage, tmp))
        global flag, label
        label = np.vstack((label, [[flag]]))
        if flag == 0:
            cv2.circle(image, (x, y), 1, (255, 255, 255), thickness=-1)
        else:
            cv2.circle(image, (x, y), 1, (0, 0, 0), thickness=-1)
        cv2.imshow("wdname", image)
        time.sleep(0.1)


def SVM():
    svm = cv2.ml.SVM_create()
    svm.setType(cv2.ml.SVM_C_SVC)
    svm.setKernel(cv2.ml.SVM_RBF)
    svm.setC(10.0)
    svm.setGamma(0.01)
    global targetImage
    targetImage = np.array(targetImage, dtype='float32')
    svm.train(targetImage, cv2.ml.ROW_SAMPLE, label)
    svm.save("svm_l.xml")
    global image
    cv2.namedWindow("im2", 0)
    im2 = cv2.imread("redball.jpg")
    cv2.imshow("im2", im2)
    result = np.ones((im2.shape[0], im2.shape[1]), dtype=np.uint8)
    result[:, :] = 0
    for i in range(0, im2.shape[0] - 1, 3):
        for j in range(0, im2.shape[1] - 1, 3):
            point = im2[i, j]
            sampleMat = np.vstack([point])
            sampleMat = np.array(sampleMat, dtype='float32')
            (c, response) = svm.predict(sampleMat)
            if response == 1:
                result[i, j] = 255

    cv2.namedWindow("result", 0)
    cv2.imshow("result", result)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    result = cv2.dilate(result, kernel, iterations=1)
    result = cv2.dilate(result, kernel, iterations=1)
    result = cv2.erode(result, kernel, iterations=1)
    contours, hier = cv2.findContours(result, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cmaxIdx = 0
    if len(contours) > 0:
        for i in range(0, len(contours)):
            if cv2.contourArea(contours[i]) > 330 * 220:
                cmaxIdx = i
        t = cmaxIdx
        cmaxIdx = cmaxIdx - 1
        for i in range(0, len(contours)):
            if cv2.contourArea(contours[i]) > cv2.contourArea(contours[cmaxIdx]) and i != t:
                cmaxIdx = i
        x, y, w, h = cv2.boundingRect(contours[cmaxIdx])
        cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        down_y = y + h
        print down_y
        print(w, h)
        cv2.namedWindow("SVM", 0)
        cv2.imshow("SVM", im2)


if __name__ == "__main__":
    image = cv2.imread('redball.jpg')
    main(image)
    cv2.waitKey(0)
