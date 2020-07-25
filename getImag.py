# -*- encoding: utf-8 -*-
"""
@File    :   getImag.py

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/25 下午10:16

@Author :   赵方国
"""


import random
import math
import time
import argparse

import numpy as np
import cv2
import motion
import almath
from naoqi import ALProxy
import vision_definitions

IP = '169.254.202.17'
PORT = 9559


def getImag(IP, PORT, cameraID, name):
    """
    得到图片一张

    :param IP: 机器人IP
    :param PORT: 9559
    :param cameraID: 0为上摄像头，1为下摄像头
    :param name: 相机名称，一般由随机数生成
    :return: 图片一张
    """
    camProxy = ALProxy("ALVideoDevice", IP, PORT)
    resolution = vision_definitions.kQVGA
    colorSpace = vision_definitions.kBGRColorSpace
    fps = 20
    print "Is camera opened ?", camProxy.isCameraOpen(1)
    print "getting images in remote"
    nameID = camProxy.subscribe(name, resolution, colorSpace, fps)
    camProxy.setActiveCamera(cameraID)
    img = camProxy.getImageRemote(nameID)
    imagHeader0 = np.array(img[6])
    imagHeader = map(ord, img[6])
    camProxy.releaseImage(nameID)
    imagHeader = np.reshape(imagHeader, [240, 320, 3])
    img = np.uint8(imagHeader)
    cv2.imshow(name, img)
    return img


if __name__ == "__main__":
    robotIP = '169.254.48.157'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    imag = getImag(robotIP, 9559, 1, 'ajgkhkcjkfyljif')
    cv2.imwrite('hole_afternoon4.jpg', imag)
    motionProxy.rest()
    cv2.waitKey(0)
