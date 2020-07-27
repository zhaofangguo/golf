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
from naoqi import ALProxy
from getImag import getImag
import random
from ImagProgressHSV import ImagProgressHSV
from turnHeadandGetDistance import turnHeadandGetDistance
from turn90andFindtheHole import turn90andFindtheHole
from distance import getangle


def walkToBall(robotIP, PORT):
    """
    该函数将得到机器人与球的距离，走近球，判断是否能看到洞，不能则绕着球90度转直到看到洞,函数结束

    :param robotIP: IP
    :param PORT: 9559
    :return: True
    """
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    smallTurnStep = [["StepHeight", 0.01], ["MaxStepX", 0.03]]
    distance = turnHeadandGetDistance(robotIP, PORT)[2]
    rotationYaw = motionProxy.getAngles('HeadYaw', True)
    distance = distance / 1000 - 0.4  # TODO 此处距离依靠新测距函数准确度
    rotationYaw = float(str(rotationYaw)[1:10])
    rotationYaw = rotationYaw * almath.TO_RAD
    # motionProxy.moveTo(0, 0, rotationYaw, smallTurnStep)
    postureProxy.goToPosture("StandInit", 0.5)
    motionProxy.moveTo(distance, 0, 0, smallTurnStep)
    turn90andFindtheHole(robotIP, PORT, distance)
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
    time.sleep(2)
    walkToBall(robotIP, PORT)
