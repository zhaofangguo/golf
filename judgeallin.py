# coding=utf-8
"""
判断是否在视野中同时存在球和洞
不存在则一直原地转圈，直到同时存在
"""
import time

from ImagProgressHSV import ImagProgressHSV
from ImagProgressSVM import ImagProgressSVM
from getImag import getImag
from naoqi import ALProxy
from cmath import pi
import cv2 as cv


def judgeallin(robotIP, PORT):
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    img = getImag(robotIP, PORT, 0, 'alkagjhie')
    # flag = (ImagProgressHSV(img, 'hole') is not None) and (ImagProgressHSV(img, 'ball') is not None)
    flag = (ImagProgressSVM(img, 'hole') is not None) and (ImagProgressSVM(img, 'ball') is not None)
    if flag:
        tts.say('find all in')
        return True
    else:
        while not flag:
            motionProxy.moveTo(0, 0, pi / 3)
            # flag = (ImagProgressHSV(img, 'hole') is not None) and (ImagProgressHSV(img, 'ball') is not None)
            flag = (ImagProgressSVM(img, 'hole') is not None) and (ImagProgressSVM(img, 'ball') is not None)
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
