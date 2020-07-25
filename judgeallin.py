# -*- encoding: utf-8 -*-
"""
@File    :   judgeallin.py

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/25 下午10:16

@Author :   赵方国
"""


import time

from ImagProgressHSV import ImagProgressHSV
from getImag import getImag
from naoqi import ALProxy
from cmath import pi
import cv2 as cv


def judgeallin(robotIP, PORT):
    """
    判断是否在视野中同时有球和球洞，没有则一直以60度为周期旋转直到同时出现在视野中

    :param robotIP: 机器人IP
    :param PORT: 9559
    :return: TRUE，同时出现在视野中
    """
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    img = getImag(robotIP, PORT, 0, 'alkagjhie')
    flag = (ImagProgressHSV(img, 'hole') is not None) and (ImagProgressHSV(img, 'ball') is not None)
    # flag = (ImagProgressSVM(img, 'hole') is not None) and (ImagProgressSVM(img, 'ball') is not None)
    if flag:
        tts.say('find all in')
        return True
    else:
        while not flag:
            motionProxy.moveTo(0, 0, pi / 3)
            flag = (ImagProgressHSV(img, 'hole') is not None) and (ImagProgressHSV(img, 'ball') is not None)
            # flag = (ImagProgressSVM(img, 'hole') is not None) and (ImagProgressSVM(img, 'ball') is not None)
            tts.say('not find all in')
            time.sleep(0.5)
        return True


if __name__ == '__main__':
    robotIP = '169.254.202.17'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    print judgeallin(robotIP, 9559)
