# -*- encoding: utf-8 -*-
"""
@File    :   findHole.py

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/25 下午10:16

@Author :   赵方国
"""


import math
import random
from cmath import pi

import cv2 as cv
from naoqi import ALProxy

from mircoadjust import mircoadjust
from turnHeadandGetDistance import turnHeadandGetDistance
from ImagProgressHSV import ImagProgressHSV
from distance import getangle
from getImag import getImag






# 该py为检测洞和球的x是否在一条直线上

def findHole(robotIP, PORT=9559):
    """
    找洞和球的关系，平移直到机器人位于洞和球的平分线上，然后机器人旋转，走到球的后方，微调对准球和球洞

    :param robotIP: 机器人的IP地址
    :param PORT: 9559
    :return: TRUE，返回时机器人已经与球和球门对齐，下一步直接击球
    """
    # 获取代理
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    # 获取当前头部角度
    rotation1 = motionProxy.getAngles('HeadYaw', True)
    rotation2 = motionProxy.getAngles('HeadPitch', True)
    name = str(random.randint(1, 1000))
    img = getImag(robotIP, PORT, 1, name)
    # 获取球和洞的角度
    anglelist = getangle(ImagProgressHSV(img, 'hole', 1), rotation1, rotation2)
    alphahole = float(anglelist[0])
    anglelist = getangle(ImagProgressHSV(img, 'ball', 1), rotation1, rotation2)
    alphaball = float(anglelist[0])
    alpha = abs(alphahole - alphaball)
    legName = ["LLeg", "RLeg"]
    X = 0
    Y = 0.05
    Theta = 0
    footSteps = [[X, Y, Theta]]
    fractionMaxSpeed = [1.0]
    clearExisting = False
    # 进行左右平移直到处于垂直平分线
    if abs(alphaball) > abs(alphahole) and alpha > pi / 180 * 5:
        tts.say('move to ball')
        # motionProxy.moveTo(0, 0.02 * alphaball / abs(alphaball), 0)
        if alphaball < 0:
            motionProxy.setFootStepsWithSpeed(legName[0], footSteps, fractionMaxSpeed, clearExisting)
        else:
            motionProxy.setFootStepsWithSpeed(legName[1], footSteps, fractionMaxSpeed, clearExisting)
        findHole(robotIP, PORT)
    elif abs(alphaball) < abs(alphahole) and alpha > pi / 180 * 5:
        tts.say('move to hole')
        # motionProxy.moveTo(0, 0.02 * alphahole / abs(alphahole), 0)
        if alphahole < 0:
            motionProxy.setFootStepsWithSpeed(legName[0], footSteps, fractionMaxSpeed, clearExisting)
        else:
            motionProxy.setFootStepsWithSpeed(legName[1], footSteps, fractionMaxSpeed, clearExisting)

        findHole(robotIP, PORT)
    else:
        tts.say('do not need to move')
        alphamiddle = (pi - abs(alphahole) * 2) / 2
        distance = turnHeadandGetDistance(robotIP, PORT)  # 头部已转向物体中心
        distance = distance / 1000 - 0.2  # 此处为经验值，需要调整，在先前的测距中，测的距离会比真实距离小10厘米左右
        x = distance * math.sin(alphamiddle)
        y = distance * math.cos(alphamiddle) + distance
        tts.say('move behind ball')
        postureProxy.goToPosture("StandInit", 0.5)
        # anglelist = getangle(ImagProgressHSV(img, 'ball', 1), rotation1, rotation2)
        # anglelist = getangle(ImagProgressSVM(img, 'ball'), rotation1, rotation2)
        # alphaball = float(anglelist[0])
        motionProxy.moveTo(x, y * alphaball * abs(alphaball), 0)
        tts.say('turn to ball')
        motionProxy.moveTo(0, 0, pi / 2)
        image = getImag(robotIP, PORT, 1, name)
        ball = ImagProgressHSV(image, 'ball', 1)
        hole = ImagProgressHSV(image, 'hole', 1)
        flag = True
        while flag:
            flag = mircoadjust(ball, hole, robotIP)
        tts.say('ready to kick')
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
    robotIP = '169.254.223.247'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    findHole(robotIP, 9559)
