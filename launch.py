# -*- encoding: utf-8 -*-
"""
@File    :   launch.py

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/25 下午10:16

@Author :   赵方国
"""


from judgeallin import judgeallin
from kick import kick
from naoqi import ALProxy
import cv2 as cv
from getImag import getImag
from ImagProgressHSV import ImagProgressHSV
from turnHeadandGetDistance import turnHeadandGetDistance
from areajudgement import areajudgement
from findHole import findHole
import random
from cmath import pi
import time


def main(robotIP, PORT=9559):
    """
    整个流程的入口函数，执行一整套动作

    :param robotIP: 机器人IP
    :param PORT: 9559
    :return: 无返回值
    """
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    if judgeallin(robotIP, PORT):
        findHole(robotIP, PORT)
        tts.say('ready to kick')
        distance = turnHeadandGetDistance(robotIP, PORT)
        name = str(random.randint(1,1000))
        area = areajudgement(getImag(robotIP, PORT, 1, name))
        while area < 1000:
            motionProxy.moveTo(0.05, 0, 0)
        else:
            pass
        kick()
        tts.say('kick finish')
    motionProxy.rest()


if __name__ == '__main__':
    main('169.254.202.17', 9559)
