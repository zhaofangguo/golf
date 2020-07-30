# -*- encoding: utf-8 -*-
"""
@File    :   walkToBall.py    

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/27 下午4:03 

@Author :   赵方国        
"""
import time

import cv2 as cv

import almath
from getImagfromvedio import getImagfromvedio
from naoqi import ALProxy
from getImag import getImag
import random
from ImagProgressHSV import ImagProgressHSV
from numpy import pi
from turnHeadandGetDistance import turnHeadandGetDistance
from turn90andFindtheHole import turn90andFindtheHole
from distance import getangle


def walkToBall(robotIP, PORT):
    """
    该函数由球心在图片中的x位置决定是否进行旋转直到球位于视野中心，然后判断球的y坐标的位置，走到相应的距离，执行找洞函数

    :param robotIP: IP
    :param PORT: 9559
    :return: True
    """
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    smallTurnStep = [["StepHeight", 0.01], ["MaxStepX", 0.03]]
    while True:
        ball = ImagProgressHSV(getImagfromvedio(robotIP, PORT), 'ball', 1)[0]
        motionProxy.moveTo(0, 0, pi / 6, smallTurnStep)
        if 140 < ball[0] < 180:
            break
    y = ball[1]
    # TODO 此处的24个距离值需要具体给定
    distance = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05,
                0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
    y = y // 10
    flag = -(float(ball[0]) - 160) / abs(float(ball[0]) - 160)
    motionProxy.moveTo(distance[y], flag * 0.2, 0, smallTurnStep)
    # distance = turnHeadandGetDistance(robotIP, PORT)[2]
    # rotationYaw = motionProxy.getAngles('HeadYaw', True)
    # distance = distance / 100
    # rotationYaw = float(str(rotationYaw)[1:10])
    # rotationYaw = rotationYaw * almath.TO_RAD
    # # motionProxy.moveTo(0, 0, rotationYaw, smallTurnStep)
    # postureProxy.goToPosture("StandInit", 0.5)
    # # if not 80 < ImagProgressHSV(getImag(robotIP, PORT, 0, str(random.randint(1, 1000))), 'ball', 0)[0][0] < 240:
    # #     rotationYaw = motionProxy.getAngles('HeadYaw', True)
    # #     motionProxy.moveTo(0, 0, rotationYaw, smallTurnStep)
    # motionProxy.moveTo(distance, 0, 0, smallTurnStep)
    turn90andFindtheHole(robotIP, PORT, 0.2)
    tts.say('walk to ball finish')
    return True


def walkToballv2(robotIP, PORT):
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    smallTurnStep = [["StepHeight", 0.01], ["MaxStepX", 0.03]]  # 单步移动
    data = ImagProgressHSV(getImagfromvedio(robotIP, PORT, 0), 'ball', 0)[0]
    ball = data[0]
    hole = data[1]
    if 140 < ball < 180:
        motionProxy.moveTo(0, 0, 0, smallTurnStep)
    if ball[0] < hole[0]:
        while not (140 < ball < 180):
            motionProxy.moveTo(0, 0, pi / 6, smallTurnStep)
    elif ball[0] > hole[0]:
        while not (140 < ball < 180):
            motionProxy.moveTo(0, 0, -pi / 6, smallTurnStep)


if __name__ == '__main__':
    robotIP = '169.254.202.17'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    smallTurnStep = [["StepHeight", 0.01], ["MaxStepX", 0.03]]  # 单步移动
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    time.sleep(2)
    walkToBall(robotIP, PORT)
