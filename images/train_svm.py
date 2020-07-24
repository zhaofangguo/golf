# -*- encoding: UTF-8 -*-
"""
从获取的拼接成一张的图片,进行训练和识别
但容易过拟合
是训练SVM的脚本，生成的xml文件会被别的脚本调用
应该生成两个xml，一个是球的，一个是洞的
目前缺少洞的训练数据集！！！！！！！！！！！！！！！
"""

import cv2
import numpy as np
import time

global label
label = [[0]]
global targetImage
targetImage = [[0, 0, 0]]


def main(imag, ballorhole):
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
    SVM(ballorhole)


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
        targetImage = np.vstack((targetImage, tmp))  # vstack函数用于拼接数组
        global flag, label
        label = np.vstack((label, [[flag]]))
        if flag == 0:
            cv2.circle(image, (x, y), 1, (255, 255, 255), thickness=-1)
        else:
            cv2.circle(image, (x, y), 1, (0, 0, 0), thickness=-1)
        cv2.imshow("wdname", image)
        # time.sleep(0.1)


# 1、提取正负样本hog特征
#
# 2、投入svm分类器训练，得到model
#
# 3、由model生成检测子
#
# 4、利用检测子检测负样本，得到hardexample
#
# 5、提取hardexample的hog特征并结合第一步中的特征一起投入训练，得到最终检测子。
def SVM(ballorhole):
    svm = cv2.ml.SVM_create()
    svm.setType(cv2.ml.SVM_C_SVC)  # c类支撑向量分类机
    # 我们在这里选择可用于n级分类的类型C_SVC（n≥2）。这种类型的重要特征是它处理非线性类效果好（即，当训练数据是非线性可分离的时）。
    # 此功能在这里并不重要，因为数据是线性可分的，我们选择此SVM类型只是最常用的。
    svm.setKernel(cv2.ml.SVM_RBF)  # 径向积核函数，高斯核函数
    svm.setC(10.0)
    svm.setGamma(0.01)
    global targetImage
    targetImage = np.array(targetImage, dtype='float32')
    svm.train(targetImage, cv2.ml.ROW_SAMPLE, label)
    # train函数建立SVM模型，第一个参数为训练数据，第二个参数为分类结果，最后一个参数即CvSVMParams
    if ballorhole == 'ball':
        svm.save("svm_ball_morining.xml")
    else:
        svm.save("svm_hole.xml")
    global image
    cv2.namedWindow("im2", 0)
    im2 = cv2.imread("final.jpg")
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
    image = cv2.imread('finalafterhole.jpg')
    # main(image, 'ball')
    main(image, 'hole')
    cv2.waitKey(0)
