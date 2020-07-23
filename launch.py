# coding=utf-8
"""
最终launch文件，直接运行则可以完成整套动作
"""
from judgeallin import judgeallin
from kick import kick
from naoqi import ALProxy
import cv2 as cv
from getImag import getImag
from ImagProgressHSV import ImagProgressHSV
from turnHeadandGetDistance import turnHeadandGetDistance
from findHole import findHole
import random
from cmath import pi
import time


def main(robotIP, PORT=9559):
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    if judgeallin(robotIP, PORT):
        findHole(robotIP, PORT)
        distance = turnHeadandGetDistance(robotIP, PORT)
        distance = distance / 10 - 0.1
        motionProxy.moveTo(distance - 0.2, 0, 0)
        kick()


if __name__ == '__main__':
    main('169.254.202.17', 9559)
