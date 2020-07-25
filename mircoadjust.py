# -*- encoding: utf-8 -*-
"""
@File    :   mircoadjust.py

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/25 下午10:16

@Author :   赵方国
"""


from distance import getangle
from naoqi import ALProxy
from ImagProgressHSV import ImagProgressHSV


def mircoadjust(ball, hole, robotIP):
    """
    击球前的微调函数，左右移动直到球和球洞在一条直线上

    :param ball: 由ImagProgressHSV函数返回的球的x，y坐标
    :param hole: 由ImagProgressHSV函数返回的洞的x，y坐标
    :param robotIP: 机器人IP
    :return: True代表已经对齐，False代表还没有对齐
    """
    motionProxy = ALProxy("ALMotion", robotIP, 9559)
    legName = ["LLeg", "RLeg"]
    X = 0
    Y = 0.02
    Theta = 0
    footSteps = [[X, Y, Theta]]
    fractionMaxSpeed = [1.0]
    clearExisting = False
    xdistance = abs(ball[0] - hole[0]) < 20
    if xdistance:
        return True
    elif ball[0] < hole[0]:
        motionProxy.setFootStepsWithSpeed(legName[0], footSteps, fractionMaxSpeed, clearExisting)
        return False
    elif ball[0] > hole[0]:
        footSteps = [[X, -Y, Theta]]
        motionProxy.setFootStepsWithSpeed(legName[0], footSteps, fractionMaxSpeed, clearExisting)
        return False


if __name__ == "__main__":
    robotIP = '169.254.223.247'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    mircoadjust(robotIP, 9559)
