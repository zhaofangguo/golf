# -*- encoding: utf-8 -*-
"""
@File    :   judgecircle.py    

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/27 下午8:45 

@Author :   赵方国        
"""
import cv2 as cv
import numpy as np
from naoqi import ALProxy


def judgecircle(frame, data):
    """
    该函数将计算roi区域中的红绿颜色比，若在0.7和0.9之间，则返回真值，借此判断是否霍夫变换求得是真的球

    :param frame: 一张彩色源图
    :param data: 霍夫变换求得的数组，为【圆心x坐标，圆心y坐标，圆半径】
    :return: 当判断为真实红球时，返回真值
    """
    x = int(data[0])
    y = int(data[1])
    r = int(data[2])
    a = int(y - 2 * r)
    b = int(y + 2 * r)
    c = int(x - 2 * r)
    d = int(x + 2 * r)

    print a, b, c, d
    if a < 0:
        a = 0
    if b > 120:
        b = 120
    if c < 0:
        c = 0
    if d > 160:
        d = 160
    y = a+b
    x = c+d
    roi = frame[41:93, 168:220]
    # print roi
    print frame[41:93, 168:220]
    roihsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
    lowarraygreen = np.array([30, 43, 46])
    higharraygreen = np.array([80, 255, 255])
    roiyuzhi = cv.inRange(roihsv, lowarraygreen, higharraygreen)
    count = 0
    for row in range(240):
        for col in range(320):
            pv = roiyuzhi[row, col]
            if pv == 0:
                count += 1
    flag = float(count) / float(y * x)
    print 'flag'
    print flag
    if 0.2 < flag < 0.3:
        return True
    else:
        return False


if __name__ == '__mian__':
    robotIP = '169.254.202.17'
    PORT = 9559
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    smallTurnStep = [["StepHeight", 0.01], ["MaxStepX", 0.03]]  # 单步移动
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    time.sleep(1)
    data = ImagProgressHSV(getImag(robotIP, PORT, 1, str(random.randint(1, 1000))), 'ball', 1)[0]
    print getdistancefromcam(robotIP, PORT, data)