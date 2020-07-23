# coding=utf-8
"""
转头使目标位于视野中心并计算距离
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
    """获取代理"""
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
    anglelist = getangle(ImagProgressHSV(img, 'ball'), rotation1, rotation2)
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
    img = getImag(robotIP, PORT, 1, name)
    theta = motionProxy.getAngles('HeadPitch', True)
    distance = getdistance(theta)
    print distance
    # cv.imshow('rs',img)

    # time.sleep(4.0)
    # motionProxy.rest()
    # cv.waitKey(0)
    return float(distance)


if __name__ == "__main__":
    robotIP = '169.254.202.17'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    turnHeadandGetDistance(robotIP='169.254.202.17', PORT=9559)
