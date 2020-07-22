# coding=utf-8
from cmath import pi
from cmath import tan
import almath
# getangle函数得到机器人头部相对于中心点的偏转角度，alpha是竖直方向，beta是水平方向
# getdistance函数得到距离障碍物的距离


def getangle(data, rotation1, rotation2):
    x = data[0]
    y = data[1]
    rot1 = str(rotation1)
    rot2 = str(rotation2)
    rot1 = rot1[1:5]
    rot2 = rot2[1:5]
    alpha = ((160 - float(x)) / 320) * 60.97 * pi / 180 + float(rot1)
    beta = ((float(y) - 120) / 240) * 47.64 * pi / 180 + float(rot2)
    angle = [alpha, beta]
    return angle


def getdistance(theta):
    PAI = 39.7 * almath.TO_RAD
    H = 574
    S = str(theta)
    L = 530
    distance = (float(H) - float(L)) / tan(float(PAI) + float(S))
    return distance
