from ImagProgress import ImagProgress
from distance import getangle
from distance import getdistance
from naoqi import ALProxy
from getImag import getImag
import random
import cv2 as cv
import time
import motion


def main(robotIP, PORT=9559):
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    rotation1 = motionProxy.getAngles('HeadYaw', True)
    rotation2 = motionProxy.getAngles('HeadPitch', True)
    print rotation1, rotation2
    name = random.randint(1, 1000)
    name = str(name)
    img = getImag(robotIP, PORT, 1, name)
    anglelist = getangle(ImagProgress(img), rotation1, rotation2)
    alpha = float(anglelist[0])
    beta = float(anglelist[1])
    print alpha, beta
    motionProxy.setStiffnesses("Head", 1.0)

    # Example showing a single target angle for one joint
    # Interpolates the head yaw to 1.0 radian in 1.0 second
    names = "HeadYaw"
    angleLists = alpha
    timeLists = 1.0
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    print 'Yaw finish'
    names = "HeadPitch"
    angleLists = beta
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    print 'Pitch finish'

    time.sleep(1.0)
    img = getImag(robotIP, PORT, 1, name)
    theta = motionProxy.getAngles('HeadPitch', True)
    distance = getdistance(theta)
    print distance
    cv.imshow('rs',img)


    # time.sleep(4.0)
    motionProxy.rest()
    cv.waitKey(0)


if __name__ == "__main__":
    main(robotIP='169.254.202.17', PORT=9559)