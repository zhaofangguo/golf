# -*- encoding: utf-8 -*-
"""
@File    :   seachForBall.py    

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/28 上午11:31 

@Author :   赵方国        
"""
import math
import random

from getImagfromvedio import getImagfromvedio
from naoqi import ALProxy
from ImagProgressHSV import ImagProgressHSV
from getImag import getImag


def searchForBall(robotIP, PORT):
    """
    此函数在流程开始前进行找球，采用原地转圈的形式，一旦找到球，停止动作

    :param robotIP: IP
    :param PORT: 9559
    :return: True，在找到球的时候返回
    """
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    tts.say('search for ball')
    smallTurnStep = [["StepHeight", 0.01], ["MaxStepX", 0.03]]
    # TODO 此处是否需要改为视频流需要依据实际效果进行调整
    try:
        data = ImagProgressHSV(getImagfromvedio(robotIP, PORT, 1), 'ball', 0)[0][0]
        tts.say('find the ball')
        return True
    except TypeError:
        tts.say('can not find the ball')
        motionProxy.moveTo(0, 0, math.pi / 3, smallTurnStep)
        return searchForBall(robotIP, PORT)


if __name__ == '__main__':
    robotIP = '169.254.252.60'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    smallTurnStep = [["StepHeight", 0.01], ["MaxStepX", 0.03]]  # 单步移动
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    searchForBall(robotIP, PORT)
