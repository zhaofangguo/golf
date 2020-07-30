# -*- encoding: utf-8 -*-
"""
@File    :   turn90andFindtheHole.py    

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/27 下午4:21 

@Author :   赵方国        
"""

import cv2 as cv

from getImagfromvedio import getImagfromvedio
from naoqi import ALProxy
from getImag import getImag
from cmath import pi
import random
from ImagProgressHSV import ImagProgressHSV
from turnHeadandGetDistance import turnHeadandGetDistance
from distance import getangle


def turn90andFindtheHole(robotIP, PORT, distance):
    """
    该函数将绕着给定的距离进行90度绕圈找洞，直到找到洞返回

    :param robotIP: IP
    :param PORT: 9559
    :param distance: 距离值，一般由turnHeadandGetDistance()函数得到
    :return: True表示动作执行结束
    """
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    smallTurnStep = [["StepHeight", 0.01], ["MaxStepX", 0.03]]
    hole = ImagProgressHSV(getImagfromvedio(robotIP, PORT, 0), 'hole', 0)[0][1]
    print hole
    if hole != [0, 0]:
        tts.say('do not need to move')
        return True
    motionProxy.moveTo(distance, -distance, pi / 2, smallTurnStep)
    tts.say('finish')
    hole = ImagProgressHSV(getImagfromvedio(robotIP, PORT, 0), 'hole', 0)[0][1]
    while hole == [0, 0]:
        motionProxy.moveTo(distance, -distance, pi / 2, smallTurnStep)
        hole = ImagProgressHSV(getImagfromvedio(robotIP, PORT, 0), 'hole', 0)[0][1]
    return True


if __name__ == '__main__':
    robotIP = '169.254.202.17'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    smallTurnStep = [["StepHeight", 0.01], ["MaxStepX", 0.03]]  # 单步移动
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    distance = turnHeadandGetDistance(robotIP, PORT)[2]
    distance = float(distance) - 0.4
    turn90andFindtheHole(robotIP, PORT, distance)
    cv.waitKey(0)
