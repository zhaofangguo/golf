from ImagProgress import ImagProgress
from distance import getangle
from naoqi import ALProxy
from getImag import getImag
import random
import time
import motion


def main(robotIP, PORT=9559):
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    rotation1 = motionProxy.getAngles('HeadYaw', True)
    rotation2 = motionProxy.getAngles('HeadPitch', True)
    img = getImag(robotIP, PORT, 0)
    anglelist = getangle(ImagProgress(img), rotation1, rotation2)
    alpha = int(anglelist[0])
    beta = int(anglelist[1])

    chainName = "HeadYaw"
    frame = motion.FRAME_TORSO
    position = [0.0, 0.0, 0, alpha, 0.0, 0]  # Absolute Position
    fractionMaxSpeed = 0.2
    axisMask = 56
    motionProxy.setPositions(chainName, frame, position, fractionMaxSpeed, axisMask)
    chainName = "HeadPitch"
    frame = motion.FRAME_TORSO
    position = [0.0, 0.0, 0, 0.0, beta, 0]  # Absolute Position
    fractionMaxSpeed = 0.2
    axisMask = 56
    motionProxy.setPositions(chainName, frame, position, fractionMaxSpeed, axisMask)

    time.sleep(4.0)
    motionProxy.rest()


if __name__ == "__main__":
    main(robotIP='169.254.202.17', PORT=9559)
