# coding=utf-8
"""
使用拍子打球的动作
"""
from naoqi import ALProxy


def kick(robotIP, PORT=9559):
    # Choregraphe simplified export in Python.
    from naoqi import ALProxy
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([2.4, 3.08])
    keys.append([0.0152981, 0.0152981])

    names.append("HeadYaw")
    times.append([2.4, 3.08])
    keys.append([-0.00464392, -0.00464392])

    names.append("LAnklePitch")
    times.append([2.4, 3.08])
    keys.append([-0.343658, -0.343658])

    names.append("LAnkleRoll")
    times.append([2.4, 3.08])
    keys.append([-0.00149202, -0.00149202])

    names.append("LElbowRoll")
    times.append([2.4, 3.08])
    keys.append([-0.974048, -0.974048])

    names.append("LElbowYaw")
    times.append([2.4, 3.08])
    keys.append([-1.36837, -1.36837])

    names.append("LHand")
    times.append([2.4, 3.08])
    keys.append([0.2616, 0.2616])

    names.append("LHipPitch")
    times.append([2.4, 3.08])
    keys.append([-0.454022, -0.454022])

    names.append("LHipRoll")
    times.append([2.4, 3.08])
    keys.append([0.0061779, 0.0061779])

    names.append("LHipYawPitch")
    times.append([2.4, 3.08])
    keys.append([-0.00762796, -0.00762796])

    names.append("LKneePitch")
    times.append([2.4, 3.08])
    keys.append([0.704064, 0.704064])

    names.append("LShoulderPitch")
    times.append([2.4, 3.08])
    keys.append([1.43578, 1.43578])

    names.append("LShoulderRoll")
    times.append([2.4, 3.08])
    keys.append([0.263806, 0.263806])

    names.append("LWristYaw")
    times.append([2.4, 3.08])
    keys.append([0.0137641, 0.0137641])

    names.append("RAnklePitch")
    times.append([2.4, 3.08])
    keys.append([-0.34971, -0.34971])

    names.append("RAnkleRoll")
    times.append([2.4, 3.08])
    keys.append([4.19617e-05, 4.19617e-05])

    names.append("RElbowRoll")
    times.append([2.4, 3.08])
    keys.append([1.50029, 1.4282])

    names.append("RElbowYaw")
    times.append([2.4, 3.08])
    keys.append([0.0168321, 0.0352399])

    names.append("RHand")
    times.append([2.4, 3.08])
    keys.append([0.2584, 0.2584])

    names.append("RHipPitch")
    times.append([2.4, 3.08])
    keys.append([-0.454106, -0.454106])

    names.append("RHipRoll")
    times.append([2.4, 3.08])
    keys.append([0.00310993, 0.00310993])

    names.append("RHipYawPitch")
    times.append([2.4, 3.08])
    keys.append([-0.00762796, -0.00762796])

    names.append("RKneePitch")
    times.append([2.4, 3.08])
    keys.append([0.696478, 0.696478])

    names.append("RShoulderPitch")
    times.append([2.4, 3.08])
    keys.append([0.722556, 0.759372])

    names.append("RShoulderRoll")
    times.append([2.4, 3.08])
    keys.append([-0.124296, -0.0890141])

    names.append("RWristYaw")
    times.append([2.4, 3.08])
    keys.append([0.858998, -1.37144])

    try:
        # uncomment the following line and modify the IP if you use this script outside Choregraphe.
        # motion = ALProxy("ALMotion", IP, 9559)
        motion = ALProxy("ALMotion")
        motion.angleInterpolation(names, keys, times, True)
    except BaseException, err:
        print err


    names.append("HeadPitch")
    times.append([2.4, 3.08])
    keys.append([0.0152981, 0.0152981])

    names.append("HeadYaw")
    times.append([2.4, 3.08])
    keys.append([-0.00464392, -0.00464392])

    names.append("LAnklePitch")
    times.append([2.4, 3.08])
    keys.append([-0.343658, -0.343658])

    names.append("LAnkleRoll")
    times.append([2.4, 3.08])
    keys.append([-0.00149202, -0.00149202])

    names.append("LElbowRoll")
    times.append([2.4, 3.08])
    keys.append([-0.974048, -0.974048])

    names.append("LElbowYaw")
    times.append([2.4, 3.08])
    keys.append([-1.36837, -1.36837])

    names.append("LHand")
    times.append([2.4, 3.08])
    keys.append([0.2616, 0.2616])

    names.append("LHipPitch")
    times.append([2.4, 3.08])
    keys.append([-0.454022, -0.454022])

    names.append("LHipRoll")
    times.append([2.4, 3.08])
    keys.append([0.0061779, 0.0061779])

    names.append("LHipYawPitch")
    times.append([2.4, 3.08])
    keys.append([-0.00762796, -0.00762796])

    names.append("LKneePitch")
    times.append([2.4, 3.08])
    keys.append([0.704064, 0.704064])

    names.append("LShoulderPitch")
    times.append([2.4, 3.08])
    keys.append([1.43578, 1.43578])

    names.append("LShoulderRoll")
    times.append([2.4, 3.08])
    keys.append([0.263806, 0.263806])

    names.append("LWristYaw")
    times.append([2.4, 3.08])
    keys.append([0.0137641, 0.0137641])

    names.append("RAnklePitch")
    times.append([2.4, 3.08])
    keys.append([-0.34971, -0.34971])

    names.append("RAnkleRoll")
    times.append([2.4, 3.08])
    keys.append([4.19617e-05, 4.19617e-05])

    names.append("RElbowRoll")
    times.append([2.4, 3.08])
    keys.append([1.50029, 1.4282])

    names.append("RElbowYaw")
    times.append([2.4, 3.08])
    keys.append([0.0168321, 0.0352399])

    names.append("RHand")
    times.append([2.4, 3.08])
    keys.append([0.2584, 0.2584])

    names.append("RHipPitch")
    times.append([2.4, 3.08])
    keys.append([-0.454106, -0.454106])

    names.append("RHipRoll")
    times.append([2.4, 3.08])
    keys.append([0.00310993, 0.00310993])

    names.append("RHipYawPitch")
    times.append([2.4, 3.08])
    keys.append([-0.00762796, -0.00762796])

    names.append("RKneePitch")
    times.append([2.4, 3.08])
    keys.append([0.696478, 0.696478])

    names.append("RShoulderPitch")
    times.append([2.4, 3.08])
    keys.append([0.722556, 0.759372])

    names.append("RShoulderRoll")
    times.append([2.4, 3.08])
    keys.append([-0.124296, -0.0890141])

    names.append("RWristYaw")
    times.append([2.4, 3.08])
    keys.append([0.858998, -1.37144])

    try:
      # uncomment the following line and modify the IP if you use this script outside Choregraphe.
      # motion = ALProxy("ALMotion", IP, 9559)
      motion = ALProxy("ALMotion")
      motion.angleInterpolation(names, keys, times, True)
    except BaseException, err:
      print err


if __name__ == '__main__':
    kick('169.254.202.17')
