# -*- encoding: utf-8 -*-
"""
@File    :   turnHeadandGetDistance.py

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/25 下午10:16

@Author :   赵方国
"""


from ImagProgressHSV import ImagProgressHSV
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
    转动头部使目标位于视野中心，然后测定距离

    :param robotIP: 机器人IP
    :param PORT: 9559
    :return: float类型的距离值
    """
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    # 获取初始头部角度
    rotation1 = motionProxy.getAngles('HeadYaw', True)
    rotation2 = motionProxy.getAngles('HeadPitch', True)
    print rotation1, rotation2
    name = random.randint(1, 1000)
    name = str(name)
    img = getImag(robotIP, PORT, 1, name)
    # 获取旋转所需角度
    anglelist = getangle(ImagProgressHSV(img, 'ball', 1), rotation1, rotation2)
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
    names = "HeadPitch"
    angleLists = beta
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    print 'Pitch finish'
    # 得到目前头部角度进行距离测算
    time.sleep(1.0)
    # img = getImag(robotIP, PORT, 1, name)
    # cv.imshow('afjklgei', img)
    theta = motionProxy.getAngles('HeadPitch', True)
    distance = getdistance(theta)

    distance = distance.real
    # cv.imshow('rs',img)
    print distance
    # time.sleep(4.0)
    # motionProxy.rest()
    # cv.waitKey(0)
    return float(distance)


if __name__ == "__main__":
    robotIP = '169.254.223.247'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    turnHeadandGetDistance(robotIP='169.254.223.247', PORT=9559)
    cv.waitKey(0)
