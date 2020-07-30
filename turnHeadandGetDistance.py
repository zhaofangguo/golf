# -*- encoding: utf-8 -*-
"""
@File    :   turnHeadandGetDistance.py

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/25 下午10:16

@Author :   赵方国
"""

from ImagProgressHSV import ImagProgressHSV
from getImagfromvedio import getImagfromvedio
from distance import getdistancefromcam
from distance import getangle
from distance import getdistance
from naoqi import ALProxy
from getImag import getImag
import random
import cv2 as cv
import time
import motion


def turnHeadandGetDistance(robotIP, PORT=9559):
    """
    为了减少误差，转动头部使目标位于视野中心，然后调用函数求出距离

    :param robotIP: 机器人IP
    :param PORT: 9559
    :return: 返回distance的数组，为【x直线距离，y直线距离，斜边距离】
    """
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    rotation1 = motionProxy.getAngles('HeadYaw', True)
    rotation2 = motionProxy.getAngles('HeadPitch', True)
    print rotation1, rotation2
    img = getImagfromvedio(robotIP, PORT, 1)
    # 获取旋转所需角度
    anglelist = getangle(ImagProgressHSV(img, 'ball', 1)[0][0])
    rot1 = str(rotation1)
    rot2 = str(rotation2)
    rot1 = rot1[1:10]
    rot2 = rot2[1:10]
    anglelist[0] = float(anglelist[0]) + float(rot1)
    anglelist[1] = float(anglelist[1]) + float(rot2)
    alpha = float(anglelist[0])
    beta = float(anglelist[1])
    print alpha, beta
    # 转动头部使目标位于视野中央
    motionProxy.setStiffnesses("Head", 1.0)
    names = "HeadYaw"
    angleLists = alpha
    timeLists = 1.0
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    print 'Yaw finish'
    tts.say('Yaw finish')
    names = "HeadPitch"

    angleLists = beta
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    print 'Pitch finish'
    tts.say('Pitch finish')
    # 得到目前头部角度进行距离测算
    time.sleep(1.0)
    img = getImagfromvedio(robotIP, PORT, 1)
    cv.imshow('img', img)
    data = ImagProgressHSV(img, 'ball', 1)[0][0]
    distance = getdistancefromcam(robotIP, PORT, data)
    # theta = motionProxy.getAngles('HeadPitch', True)
    # distance = getdistance(theta)
    # distance = distance.real
    # cv.imshow('rs',img)
    print distance
    # time.sleep(4.0)
    # motionProxy.rest()
    # cv.waitKey(0)
    return distance


if __name__ == "__main__":
    robotIP = '169.254.202.17'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    turnHeadandGetDistance(robotIP, PORT=9559)
    cv.waitKey(0)
