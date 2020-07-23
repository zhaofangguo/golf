from __future__ import print_function
import cv2
import numpy as np
import time

global label
label = [[0]]
global targetImage
targetImage = [[0, 0, 0]]


def main():
    global image
    image = cv2.imread("final.jpg")
    cv2.namedWindow("wdname")
    cv2.setMouseCallback("wdname", on_EVENT_LBUTTONDOWN)
    cv2.imshow("wdname", image)
    global flag
    flag = 1
    while (True):
        c = cv2.waitKey(0)
        if (c & 255) == 27:
            print("Exiting ...", sep='\n')
            cv2.destroyAllWindows()
            break
        if chr(c) == 'q':
            flag = 0
        # if chr(c) == 'q':
        #     cv2.destroyAllWindows()
        #     break
    SVM()


def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
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
            cv2.circle(image, (x, y), 1, (0, 255, 0), thickness=-1)
        cv2.imshow("wdname", image)


def SVM():
    time1 = time.time()
    svm = cv2.ml.SVM_create()
    svm.setType(cv2.ml.SVM_C_SVC)
    svm.setKernel(cv2.ml.SVM_RBF)
    svm.setC(10.0)
    svm.setGamma(0.01)
    global targetImage
    targetImage = np.array(targetImage, dtype='float32')
    svm.train(targetImage, cv2.ml.ROW_SAMPLE, label)
    svm.save("test.xml")
    global image
    im2 = cv2.imread("final.jpg")
    cv2.imshow("im2", im2)

    result = np.ones((im2.shape[0], im2.shape[1]), dtype=np.uint8)
    result[:, :] = 255
    for i in range(0, im2.shape[0] - 1, 3):
        for j in range(0, im2.shape[1] - 1, 3):
            point = im2[i, j]
            sampleMat = np.vstack([point])
            sampleMat = np.array(sampleMat, dtype='float32')
            (c, response) = svm.predict(sampleMat)
            if response == 1:
                result[i, j] = 0
    time2 = time.time()
    case = time2 - time1
    print(case)
    cv2.imshow("result", result)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
    contours, hierarchy = cv2.findContours(result, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
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
        cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 0, 0), 2)
        center_x = x + w / 2
        down_y = y + h
        print(down_y, sep='\n')
        print(w, h)
        cv2.imshow("SVM", im2)
        cv2.waitKey()


if __name__ == "__main__":
    main()
