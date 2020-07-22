from ImagProgress import ImagProgress
from getImag import getImag
from naoqi import ALProxy
from cmath import pi
import cv2 as cv


def judgeallin(robotIP, PORT):
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    img = getImag(robotIP, PORT, 0, 'alkagjhie')
    flag = (ImagProgress(img, 'hole') is not None) and (ImagProgress(img, 'ball') is not None)
    if flag:
        return True
    else:
        while not flag:
            motionProxy.setStiffnesses("Head", 1.0)
            motionProxy.moveTo(0, 0, pi / 3)
            flag = (ImagProgress(img, 'hole') is not None) and (ImagProgress(img, 'ball') is not None)
        return True


if __name__ == '__main__':
    robotIP = '169.254.202.17'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    judgeallin(robotIP, 9559)
