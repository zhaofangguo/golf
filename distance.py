# -*- encoding: utf-8 -*-
"""
@File    :   distance.py

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/25 下午10:16

@Author :   赵方国
"""
import time
from cmath import pi
from cmath import tan

import random
import cv2 as cv

from getImagfromvedio import getImagfromvedio
from naoqi import ALProxy
from ImagProgressHSV import ImagProgressHSV
from getImag import getImag
import numpy as np
from numpy.core import pi
import motion

import almath


def getangle(data):
    """
    得到头部转动的角度以将目标移至视野中心，一般被turnHeadandGetDistance函数调用

    :param data: 一般是ImagProgressHSV函数的返回值，两个元素的数组，处理过的图片中的目标物的x，y坐标
    :return: 两个元素的数组，第一项为HeadYaw角度，第二项为HeadPitch角度
    """
    x = data[0]
    y = data[1]
    alpha = ((160 - float(x)) / 320) * 60.97 * pi / 180
    beta = ((float(y) - 120) / 240) * 47.64 * pi / 180
    angle = [alpha, beta]
    return angle


def getdistance(theta):
    """
    得到目标的距离

    :param theta: 目前HeadPitch的角度
    :return: 距离
    """
    PAI = 39.7 * almath.TO_RAD
    H = 480  # 摄像头高度
    S = str(theta)
    S = S[1:10]
    L = 30  # 目标点高度
    distance = (float(H) - float(L)) / tan(float(PAI) + float(S))
    return distance


def getdistancefromcam(robotIP, PORT, data):
    """
    该函数求解距离，函数体内自带角度获取，需要传入Imagprogress函数处理过的data

    :param robotIP: IP
    :param PORT: PORT
    :param data: Imagprogress函数处理过的data
    :return: 返回distance的数组，为【x直线距离，y直线距离，斜边距离】
    """
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    cameraDirection = 49.2 / 180 * np.pi
    name = "CameraBottom"
    cameraPos = motionProxy.getPosition(name, motion.FRAME_WORLD, True)
    cameraX, cameraY, cameraHeight = cameraPos[:3]
    head_yaw, head_pitch = motionProxy.getAngles("Head", True)
    camera_pitch = head_pitch + cameraDirection
    y = float(data[1])
    x = float(data[0])
    img_pitch = (y - 120) / 240 * 47.64 / np.pi
    img_yaw = (160 - x) / 320 * 60.97 / np.pi
    ball_pitch = camera_pitch + img_pitch
    ball_yaw = img_yaw + head_yaw
    print("ball yaw = ", ball_yaw / np.pi * 180)
    dis_x = (cameraHeight - 30) / np.tan(ball_pitch) + np.sqrt(cameraX ** 2 + cameraY ** 2)
    dis = dis_x
    dis_y = dis_x * np.sin(ball_yaw)
    dis_x = dis_x * np.cos(ball_yaw)
    distance = [abs(dis_x), abs(dis_y), abs(dis)]
    return distance


if __name__ == '__main__':
    robotIP = '169.254.202.17'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    smallTurnStep = [["StepHeight", 0.01], ["MaxStepX", 0.03]]  # 单步移动
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    time.sleep(1)
    data = ImagProgressHSV(getImagfromvedio(robotIP, PORT, 1), 'ball', 1)[0][0]
    print getdistancefromcam(robotIP, PORT, data)
    cv.waitKey(0)
