# coding=utf-8
import cv2 as cv
from getImag import getImag
from ImagProgress import ImagProgress
from turnHeadandGetDistance import turnHeadandGetDistance
from distance import getangle
from naoqi import ALProxy
from cmath import pi
import math
import random


# 该py为检测洞和球的x是否在一条直线上


def findHole(robotIP, PORT=9559):
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    rotation1 = motionProxy.getAngles('HeadYaw', True)
    rotation2 = motionProxy.getAngles('HeadPitch', True)
    name = str(random.randint(1, 1000))
    img = getImag(robotIP, PORT, 0, name)
    anglelist = getangle(ImagProgress(img, 'hole'), rotation1, rotation2)
    alphahole = float(anglelist[0])
    anglelist = getangle(ImagProgress(img, 'ball'), rotation1, rotation2)
    alphaball = float(anglelist[0])
    alpha = abs(alphahole - alphaball)
    if abs(alphaball) > abs(alphahole) and alpha > pi / 180 * 5:
        motionProxy.moveTo(0, 0.05 * alphaball / abs(alphaball), 0)
        findHole(robotIP, PORT)
    elif abs(alphaball) < abs(alphahole) and alpha > pi / 180 * 5:
        motionProxy.moveTo(0, 0.05 * alphahole / abs(alphahole), 0)
        findHole(robotIP, PORT)
    else:
        alphamiddle = (pi - abs(alphahole) * 2) / 2
        distance = turnHeadandGetDistance(robotIP, PORT)
        distance = distance / 10 - 0.1
        x = distance * math.sin(alphamiddle)
        y = distance * math.cos(alphamiddle) + distance
        motionProxy.moveTo(x, y * alphaball / abs(alphaball), 0)
        motionProxy.moveTo(0, 0, pi / 2)
        return True
    # data = ImagProgress(img, 'hole')
    # if data is None:
    #     return False
    # else:
    #     Y = abs(data[0] - 160)
    #     if Y < 20:
    #         return True
    #     else:
    #         return False


if __name__ == "__main__":
    robotIP = '169.254.202.17'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    findHole(robotIP, 9559)
