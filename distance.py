# -*- encoding: utf-8 -*-
"""
@File    :   distance.py

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/25 下午10:16

@Author :   赵方国
"""


from cmath import pi
from cmath import tan

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
