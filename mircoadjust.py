# -*- encoding: utf-8 -*-
"""
@File    :   mircoadjust.py

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/25 下午10:16

@Author :   赵方国
"""

import random

import cv2 as cv
import time

from distance import getangle
from naoqi import ALProxy
from ImagProgressHSV import ImagProgressHSV
from getImag import getImag


def mircoadjust(robotIP, PORT):
    """
    该函数为方向微调函数，在找到球和洞之后进行左右平移直到球和洞处于同一条直线上并且处于视野的中心线上

    :param robotIP: IP
    :param PORT: 9559
    :return: True表示动作以完成，可以进行前后微调
    """
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    imag = getImag(robotIP, PORT, 0, str(random.randint(1, 1000)))
    ball = ImagProgressHSV(imag, 'ball', 1)
    hole = ImagProgressHSV(imag, 'hole', 0)
    legName = ["LLeg", "RLeg"]
    X = 0
    Y = 0.05
    Theta = 0
    footSteps = [[X, Y, Theta]]
    fractionMaxSpeed = [0.5]
    clearExisting = False
    print abs(ball[0] - hole[0])
    xdistance = (abs(ball[0] - hole[0]) < 5) and (abs(ball[0] - 160) < 5)
    smallTurnStep = [["StepHeight", 0.01], ["MaxStepX", 0.03]]
    if xdistance:  # 球和洞在中心直线上
        tts.say('do not need to move')
        return True
    if abs(ball[0] - hole[0]) < 5:  # 球和洞在一条直线上，但是不在中心
        if ball[0] < 160:
            tts.say('middle middle middle')
            tts.say('walk to left')
            motionProxy.moveTo(0, 0.01, 0, smallTurnStep)
            return mircoadjust(robotIP, PORT)
        elif ball[0] >= 160:
            tts.say('middle middle middle')
            tts.say('walk to right')
            motionProxy.moveTo(0, -0.01, 0, smallTurnStep)
            return mircoadjust(robotIP, PORT)
    else:  # TODO 此处需要调整，走的方向和预期不符
        # 球和洞不在同一条直线上
        if ball[0] < hole[0]:
            tts.say('walk to left')
            motionProxy.moveTo(0, 0.05, 0, smallTurnStep)
            return mircoadjust(robotIP, PORT)
        elif ball[0] > hole[0]:
            tts.say('walk to right')
            motionProxy.moveTo(0, -0.05, 0, smallTurnStep)
            return mircoadjust(robotIP, PORT)


if __name__ == "__main__":
    robotIP = '169.254.202.17'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    flag = False
    while not flag:
        name = str(random.randint(1, 1000))
        imag = getImag(robotIP, PORT, 1, name)
        ball = ImagProgressHSV(imag, 'ball', 1)[0]
        hole = ImagProgressHSV(imag, 'hole', 1)[0]
        flag = mircoadjust(ball, hole, robotIP)
        time.sleep(1)
    cv.waitKey(0)
