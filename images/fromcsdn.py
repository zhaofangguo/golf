# -*- encoding: utf-8 -*-
"""
@File    :   fromcsdn.py    

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/27 下午7:36 

@Author :   赵方国        
"""


def _updateBallPosition(self, standState):
    """
    compute and update the ball position with the ball data in frame.
    standState: "standInit" or "standUp".
    """

    bottomCameraDirection = {"standInit": 49.2 / 180 * np.pi, "standUp": 39.7 / 180 * np.pi}
    try:
            cameraDirection = 49.2 / 180 * np.pi
            cameraPos = motionProxy.getPosition(cameraName, motion.FRAME_WORLD, True)
            cameraX, cameraY, cameraHeight = cameraPos[:3]
            head_yaw, head_pitch = motionProxy.getAngles("Head", True)
            camera_pitch = head_pitch + cameraDirection
            img_pitch = (data[1] - 120) / (240) * 47.64 / 180 * np.pi
            img_yaw = (160 - data[0]) / (320) * 60.97 / 180 * np.pi
            ball_pitch = camera_pitch + img_pitch
            ball_yaw = img_yaw + head_yaw
            print("ball yaw = ", ball_yaw / np.pi * 180)
            dis_x = (cameraHeight - self._ballRadius) / np.tan(ball_pitch) + np.sqrt(cameraX ** 2 + cameraY ** 2)
            dis_y = dis_x * np.sin(ball_yaw)
            dis_x = dis_x * np.cos(ball_yaw)
            self._ballPosition["disX"] = dis_x
            self._ballPosition["disY"] = dis_y
            self._ballPosition["angle"] = ball_yaw
