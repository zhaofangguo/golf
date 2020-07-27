# -*- encoding: utf-8 -*-
"""
@File    :   judgeallin.py

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/25 下午10:16

@Author :   赵方国
"""
import random
import time

from ImagProgressHSV import ImagProgressHSV
from getImag import getImag
from naoqi import ALProxy
from cmath import pi
import cv2 as cv


def judgeallin(robotIP, PORT):
    """
    判断是否在视野中同时有球和球洞，没有则一直以60度为周期旋转直到同时出现在视野中,函数直接调用就可以达到找同时的目的

    :param robotIP: 机器人IP
    :param PORT: 9559
    :return: TRUE，同时出现在视野中
    """
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    smallTurnStep = [["StepHeight", 0.01], ["MaxStepX", 0.03]]
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    name = str(random.randint(1, 1000))
    img = getImag(robotIP, PORT, 1, name)
    print 'hole'
    print ImagProgressHSV(img, 'hole', 1)[0]
    flag = (ImagProgressHSV(img, 'ball', 1)[0] != [0, 0]) and (ImagProgressHSV(img, 'hole', 1)[0] != [0, 0])
    # flag = (ImagProgressSVM(img, 'hole') is not None) and (ImagProgressSVM(img, 'ball') is not None)
    if flag:
        tts.say('find all in')
        return True
    else:
        while not flag:
            tts.say('not find all in')
            motionProxy.moveTo(0, 0, pi / 6, smallTurnStep)
            flag = (ImagProgressHSV(img, 'ball', 1)[0] != [0, 0]) and (ImagProgressHSV(img, 'hole', 1)[0] != [0, 0])
            # flag = (ImagProgressSVM(img, 'hole') is not None) and (ImagProgressSVM(img, 'ball') is not None)
            time.sleep(0.5)
        tts.say('find all in')
        return True


if __name__ == '__main__':
    robotIP = '169.254.202.17'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    print judgeallin(robotIP, 9559)
    cv.waitKey(0)
