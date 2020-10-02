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

from getImagfromvedio import getImagfromvedio
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
    data = ImagProgressHSV(getImagfromvedio(robotIP, PORT, 1), 'ball', 1)[0]
    # imag = getImag(robotIP, PORT, 0, str(random.randint(1, 1000)))
    ball = data[0]
    hole = data[1]
    legName = ["LLeg", "RLeg"]
    X = 0
    Y = 0.05
    Theta = 0
    footSteps = [[X, Y, Theta]]
    fractionMaxSpeed = [0.5]
    clearExisting = False
    print abs(float(ball[0]) - float(hole[0]))
    print (abs(float(ball[0]) - 160) < 5)
    xdistance = (abs(float(ball[0]) - float(hole[0])) <= 5) and (abs(float(ball[0]) - 160) <= 5)
    smallTurnStep = [["StepHeight", 0.01], ["MaxStepX", 0.03]]
    if xdistance:  # 球和洞在中心直线上
        tts.say('micro judge finish')
        cv.waitKey(1)
        return True
    if abs(float(ball[0]) - float(hole[0])) >= 100:  # 球和洞在一条直线上，但是不在中心
        if float(ball[0]) < 160:
            tts.say('max value')
            tts.say('walk to left')
            motionProxy.moveTo(0, 0.3, 0, smallTurnStep)
            cv.waitKey(1)
            return mircoadjust(robotIP, PORT)
        elif float(ball[0]) >= 160:
            tts.say('max value')
            tts.say('walk to right')
            motionProxy.moveTo(0, -0.3, 0, smallTurnStep)
            cv.waitKey(1)
            return mircoadjust(robotIP, PORT)
    elif abs(float(ball[0]) - float(hole[0])) >= 50:
        # 球和洞不在同一条直线上
        if float(ball[0]) < 160:
            tts.say('second max value')
            tts.say('walk to left')
            motionProxy.moveTo(0, 0.1, 0, smallTurnStep)
            cv.waitKey(1)
            return mircoadjust(robotIP, PORT)
        elif float(ball[0]) >= 160:
            tts.say('second max value')
            tts.say('walk to right')
            motionProxy.moveTo(0, -0.1, 0, smallTurnStep)
            cv.waitKey(1)
            return mircoadjust(robotIP, PORT)
    elif abs(float(ball[0]) - float(hole[0])) >= 10:
        if float(ball[0]) < 160:
            tts.say('min value')
            tts.say('walk to left')
            motionProxy.moveTo(0, 0.05, 0, smallTurnStep)
            cv.waitKey(1)
            return mircoadjust(robotIP, PORT)
        elif float(ball[0]) >= 160:
            tts.say('min value')
            tts.say('walk to right')
            motionProxy.moveTo(0, -0.05, 0, smallTurnStep)
            cv.waitKey(1)
            return mircoadjust(robotIP, PORT)
    elif abs(float(ball[0]) - float(hole[0])) < 5:
        tts.say('micro judge finish')
        return True


if __name__ == "__main__":
    robotIP = '169.254.252.60'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    mircoadjust(robotIP, PORT)
    cv.waitKey(0)
