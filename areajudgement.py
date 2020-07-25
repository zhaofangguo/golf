# -*- encoding: utf-8 -*-
"""
@File    :   areajudgement.py

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/25 下午10:16

@Author :   赵方国
"""

from naoqi import ALProxy
import cv2

from getImag import getImag
from ImagProgressHSV import ImagProgressHSV



def areajudgement(result):
    """
    判断球在视野中的像素点个数

    :param result: 经过阈值化处理过的二值图，其中球的部分应该是黑色，其余部分为白色
    :return: 球所占的像素点个数
    """
    height = result.shape[0]
    weight = result.shape[1]
    count = 0
    for row in range(height):
        for col in range(weight):
            pv = result[row, col]
            if pv == 0:
                count += 1
    print count
    return count


if __name__ == "__main__":
    robotIP = '169.254.223.247'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    frame = getImag(robotIP, 9559, 1, 'ahhkjkjkkdghjjgi')
    data, frame =ImagProgressHSV(frame, 'ball', 1)
    print areajudgement(frame)
    cv2.waitKey(0)