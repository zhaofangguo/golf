import random

import cv2
import math
import numpy as np
from naoqi import ALProxy
import vision_definitions
from ImagProgress import ImagProgress
import time
import argparse
import motion
import almath

IP = '169.254.247.173'
PORT = 9559


def getImag(IP, PORT, cameraID):

    camProxy = ALProxy("ALVideoDevice", IP, PORT)
    motionProxy = ALProxy("ALMotion", IP, PORT)
    postureProxy = ALProxy('ALRobotPosture', IP, PORT)
    # motionProxy.wakeUp()
    # postureProxy.goToPosture('StandInit', 0.5)
    resolution = vision_definitions.kQVGA
    colorSpace = vision_definitions.kBGRColorSpace
    fps = 20
    print "Is camera opened ?", camProxy.isCameraOpen(1)
    print "getting images in remote"
    name = random.randint(1,1000)
    name = str(name)
    nameID = camProxy.subscribe(name, resolution, colorSpace, fps)
    camProxy.setActiveCamera(cameraID)
    img = camProxy.getImageRemote(nameID)
    imagHeader0 = np.array(img[6])
    imagHeader = map(ord, img[6])
    camProxy.releaseImage(nameID)
    imagHeader = np.reshape(imagHeader, [240, 320, 3])
    img = np.uint8(imagHeader)
    return img


if __name__ == "__main__":
    getImag(IP, PORT, 0, 'uiogygoiyg')
