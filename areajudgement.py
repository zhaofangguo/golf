# -*- encoding: utf-8 -*-
"""
@File    :   areajudgement.py

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/25 下午10:16

@Author :   赵方国
"""
import random

from naoqi import ALProxy
import cv2

from getImag import getImag
from ImagProgressHSV import ImagProgressHSV


def areajudgement(robotIP, PORT):
    """
    该函数将进行判断处理过的二值图中黑色部分的多少，从而向前微调和向后微调

    :param robotIP: IP
    :param PORT: 9559
    :return: True表示动作完成，可以进行下一步击球
    """
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    name = str(random.randint(1, 1000))
    result = ImagProgressHSV(getImag(robotIP, PORT, 1, name), 'ball', 1)[1]
    count = 0
    postureProxy.goToPosture("StandInit", 0.5)
    for row in range(240):
        for col in range(320):
            pv = result[row, col]
            if pv == 0:
                count += 1
    print count
    if count < 1000:
        motionProxy.moveTo(0.017, 0, 0, smallTurnStep)
        tts.say('continue')
        return areajudgement(robotIP, PORT)
    if count > 1300:
        motionProxy.moveTo(-0.017, 0, 0, smallTurnStep)
        tts.say('continue')
        return areajudgement(robotIP, PORT)
    return True


if __name__ == "__main__":
    robotIP = '169.254.202.17'
    PORT = 9559                 
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    smallTurnStep = [["StepHeight", 0.01], ["MaxStepX", 0.03]]  # 单步移动
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    areajudgement(robotIP, PORT)
    motionProxy.rest()
    cv2.waitKey(0)
