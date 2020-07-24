# coding=utf-8
"""
检测球和洞的中心是否在同一条直线上，是则返回TRUE，否则，通过平移，运动直到同一条直线上
"""


from turnHeadandGetDistance import turnHeadandGetDistance
from ImagProgressSVM import ImagProgressSVM
from ImagProgressHSV import ImagProgressHSV
from distance import getangle
from getImag import getImag
from naoqi import ALProxy
from cmath import pi
import cv2 as cv
import random
import math

# 该py为检测洞和球的x是否在一条直线上

def findHole(robotIP, PORT=9559):
    # 获取代理
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    # 获取当前头部角度
    rotation1 = motionProxy.getAngles('HeadYaw', True)
    rotation2 = motionProxy.getAngles('HeadPitch', True)
    name = str(random.randint(1, 1000))
    img = getImag(robotIP, PORT, 0, name)
    # 获取球和洞的角度
    anglelist = getangle(ImagProgressHSV(img, 'hole'), rotation1, rotation2)
    # anglelist = getangle(ImagProgressSVM(img, 'hole'), rotation1, rotation2)
    alphahole = float(anglelist[0])
    anglelist = getangle(ImagProgressHSV(img, 'ball'), rotation1, rotation2)
    # anglelist = getangle(ImagProgressSVM(img, 'ball'), rotation1, rotation2)
    alphaball = float(anglelist[0])
    alpha = abs(alphahole - alphaball)
    # 进行左右平移直到处于垂直平分线
    if abs(alphaball) > abs(alphahole) and alpha > pi / 180 * 5:
        tts.say('move to ball')
        motionProxy.moveTo(0, 0.05 * alphaball / abs(alphaball), 0)
        findHole(robotIP, PORT)
    elif abs(alphaball) < abs(alphahole) and alpha > pi / 180 * 5:
        tts.say('move to hole')
        motionProxy.moveTo(0, 0.05 * alphahole / abs(alphahole), 0)
        findHole(robotIP, PORT)
    else:
        tts.say('do not need to move')
        alphamiddle = (pi - abs(alphahole) * 2) / 2
        distance = turnHeadandGetDistance(robotIP, PORT)
        distance = distance / 10 - 0.1  # 此处为经验值，需要调整，在先前的测距中，测的距离会比真实距离小10厘米左右
        x = distance * math.sin(alphamiddle)
        y = distance * math.cos(alphamiddle) + distance
        tts.say('move behind ball')
        motionProxy.moveTo(x, y * alphaball / abs(alphaball), 0)
        tts.say('turn to ball')
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
