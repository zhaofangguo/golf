# coding=utf-8
import random

import cv2
import math
import numpy as np
from naoqi import ALProxy
import vision_definitions
import time
import argparse
import motion
import almath


# TODO 需要将视频流进行适配
def getImagfromvedio(IP, PORT, cameraID):
    """
        得到图片一张

        :param IP: 机器人IP
        :param PORT: 9559
        :param cameraID: 0为上摄像头，1为下摄像头
        :return: 图片一张
        """
    try:
        camProxy = ALProxy("ALVideoDevice", IP, PORT)
    except Exception, e:
        print "Error in transfering ALVideoDevice"
        print str(e)
        exit(1)
    try:
        motionProxy = ALProxy("ALMotion", IP, PORT)
    except Exception, e:
        print "Error in transfering ALMotion"
        print str(e)
        exit(1)

    resolution = vision_definitions.kQVGA
    colorSpace = vision_definitions.kBGRColorSpace
    fps = 20
    nameID = camProxy.subscribe(str(random.randint(1, 1000)), resolution, colorSpace, fps)
    camProxy.setActiveCamera(cameraID)
    print "Is camera opened ?", camProxy.isCameraOpen(1)
    print "getting images in remote"
    while True:
        img = camProxy.getImageRemote(nameID)
        # cv2.SetData(img,imgData[6])
        ###以下五行为将一个mat转化为np.array(存疑)，不然无法在opencv中使用
        imagHeader0 = np.array(img[6])
        imagHeader = map(ord, img[6])
        camProxy.releaseImage(nameID)
        imagHeader = np.reshape(imagHeader, [240, 320, 3])
        img = np.uint8(imagHeader)
        #
        # cv2.imshow("src", img)
        return img


if __name__ == "__main__":
    robotIP = '169.254.202.17'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    while True:
        cv2.imshow('test', getImagfromvedio(robotIP, PORT, 1))
        cv2.waitKey(10)
