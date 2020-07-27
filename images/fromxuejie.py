# coding=utf-8
x_middle = 160  # x的中点
max_breakout_area = 45000  # 面积大的不行了的break point

# hsv阈值
low_l = np.array([9, 100, 140])
high_l = np.array([65, 255, 255])

low_ll = np.array([9, 170, 140])
high_ll = np.array([65, 255, 255])

low_lll = np.array([9, 100, 140])
high_lll = np.array([65, 255, 255])

# 步态
smallTurnStep = [["StepHeight", 0.01], ["MaxStepX", 0.03]]  # 单步移动
lower_steps = [["LeftStepHeight", 0.025], ["RightStepHeight", 0.025], ["MaxStepX", 0.05]]  # 连续走动
motion_proxy.moveToward(0.5, 0.4, 0, lower_steps)
motion_proxy.moveTo(0.14, 0, 0, smallTurnStep)
# 盘子
# x_pick_plate---------左右晃动会有偏差
# y_close_to_plate-----前后距离控制的阈值
delta_x_pick_plate = 12
y_close_to_plate = 150  # ?!?
y_close_too_much = 175

value_proxy = ALProxy("ALMemory", ROBOT_IP, PORT)

bottom_camera = 1  # 走进了柱子,需要看下面的距离
k = 1
color_space = 13
fps = 10
name_string = 'whatever'+str(random.random())
name_id = cam_proxy.subscribeCamera(name_string, bottom_camera, k, color_space, fps)
motion_proxy.angleInterpolation("HeadPitch", 10 * math.pi / 180, 1.0, 1)
print 'command angles:', motion_proxy.getAngles("HeadPitch", False)
print 'sensor angles:', motion_proxy.getAngles("HeadPitch", True)

if cam_proxy.setAllParametersToDefault(0) and cam_proxy.setAllParametersToDefault(1):
    print 'set camera default'


def main():
    angle_init = value_proxy.getData("Device/SubDeviceList/InertialSensor/AngleZ/Sensor/Value")
    print 'init angle: ' + str(angle_init)
    angle = angle_init
    """to get plate"""
    i = 0
    while True:
        i += 1
        angle = value_proxy.getData("Device/SubDeviceList/InertialSensor/AngleZ/Sensor/Value")
        print 'angle: ' + str(angle), 'trurned: ' + str(angle - angle_init)
        if abs(angle - angle_init) > 10 * math.pi / 180:
            motion_proxy.moveTo(0, 0, angle - angle_init)
            print 'turn'
        # now that got the info
        result, image, contours = image_info_l()

        # deal with data
        if not len(contours):
            print 'no pole'
            motion_proxy.moveToward(0.5, 0, -0.05, lower_steps)
        else:  # find out the max area of contour(s)
            max_area = 0
            max_contour = 0
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if w * h > max_area:
                    max_area = w * h
                    max_contour = contour

            #  draw out the max one
            x, y, w, h = cv2.boundingRect(max_contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow('interest', image)

            center_x = x + w / 2
            center_down_y = y + h
            area = w * h
            print 'center_x:'+str(center_x), 'center_down_y:'+str(center_down_y), 'area:'+str(area)

            # 走向盘子,到一个合适的位置
            if area > max_breakout_area:  # 怼的太近了
                # 以下是修正, 微调
                if center_down_y > y_close_too_much:  # 往后退
                    motion_proxy.moveTo(-0.05, 0, 0, smallTurnStep)
                    print 'adjust back off'  # 战术后退
                else:  # just in case:vision sucks & route skewing
                    print 'Stop from area, something\'wrong, maybe the vision'
                    break
                if center_x > x_middle + delta_x_pick_plate:  # 向右跨
                    motion_proxy.moveTo(0, -0.05, 0, smallTurnStep)
                    print 'adjust Right'
                if center_x < x_middle - delta_x_pick_plate:  # 向左跨
                    motion_proxy.moveTo(0, 0.05, 0, smallTurnStep)
                    print 'adjust Left'
            elif center_down_y >= y_close_to_plate and\
                    x_middle - delta_x_pick_plate <= center_x <= x_middle + delta_x_pick_plate and\
                    area > 10000:  # x&y的值合适了 补加一个修复的bug 这个area是意外 视觉的锅
                print 'Stop from x&y'
                break
            elif center_x > x_middle + delta_x_pick_plate and center_down_y < y_close_to_plate:
                motion_proxy.moveToward(0.5, -0.4, 0, lower_steps)
                print 'Right Front'
            elif center_x < x_middle - delta_x_pick_plate and center_down_y < y_close_to_plate:
                motion_proxy.moveToward(0.5, 0.4, 0, lower_steps)
                print 'Left Front'
            elif x_middle - delta_x_pick_plate <= center_x <= x_middle + delta_x_pick_plate:
                motion_proxy.moveToward(0.5, 0, -0.05, lower_steps)
                print 'Toward'
            elif center_x > x_middle + delta_x_pick_plate:
                motion_proxy.moveToward(0, -0.5, 0, lower_steps)
                print 'Right'
            elif center_x < x_middle - delta_x_pick_plate:
                motion_proxy.moveToward(0, 0.5, 0, lower_steps)
                print 'Left'

       print 'out adjust Left'
    # 在这儿微调
    motion_proxy.moveTo(0.017, 0, 0, smallTurnStep)  # 前进一小步
    print '前进一小步'
    motion_proxy.moveToward(0, 0, 0)

    print 'sensor angles:', motion_proxy.getAngles("HeadPitch", True)
    print 'ready to catch plate'

    # cv2.waitKey(0)
    motion_proxy.moveTo(0, 0.11, 0, smallTurnStep)  # 往左移
   motion_proxy.setMoveArmsEnabled(1, 0)  # 锁死右手臂,左手臂仍然活泛
    print 'pickup'
    # cv2.waitKey(0)
    motion_proxy.moveToward(0, 0, 0)
    motion_proxy.moveTo(-0.06, 0, 0, smallTurnStep)  # 后退

            motion_proxy.moveToward(0.5, 0, -0.03, lower_steps)
            elif center_x > x_middle + delta_x_pick_plate and center_down_y < y_close_to_plate:
                motion_proxy.moveToward(0.5, -0.4, 0, lower_steps)
                print 'Right Front'
            elif center_x < x_middle - delta_x_pick_plate and center_down_y < y_close_to_plate:
                motion_proxy.moveToward(0.5, 0.4, 0, lower_steps)
                print 'Left Front'
            elif x_middle - delta_x_pick_plate <= center_x <= x_middle + delta_x_pick_plate:
                motion_proxy.moveToward(0.5, 0, -0.03, lower_steps)
                print 'Toward'
            elif center_x > x_middle + delta_x_pick_plate:
                motion_proxy.moveToward(0, -0.5, 0, lower_steps)
                print 'Right'
            elif center_x < x_middle - delta_x_pick_plate:
                motion_proxy.moveToward(0, 0.5, 0, lower_steps)

            motion_proxy.moveToward(0, 0, 0)
    motion_proxy.moveToward(0, 0, 0)  # 头回去了
             print 'no pole'
            motion_proxy.moveToward(0.5, 0, -0.03, lower_steps)

                if center_down_y > y_close_too_much:  # 往后退
                    motion_proxy.moveTo(-0.08, 0, 0, smallTurnStep)

                if center_x > x_middle + delta_x_pick_plate:  # 向右跨
                    motion_proxy.moveTo(0, -0.08, 0, smallTurnStep)
                    print 'adjust Right'
                if center_x > x_middle + delta_x_pick_plate:  # 向左跨
                    motion_proxy.moveTo(0, 0.08, 0, smallTurnStep)
                    print 'adjust Left'
            elif center_x > x_middle + delta_x_pick_plate and center_down_y < y_close_to_plate:
                motion_proxy.moveToward(0.5, -0.4, 0, lower_steps)
                print 'Right Front'
            elif center_x < x_middle - delta_x_pick_plate and center_down_y < y_close_to_plate:
                motion_proxy.moveToward(0.5, 0.4, 0, lower_steps)
                print 'Left Front'
            elif x_middle - delta_x_pick_plate <= center_x <= x_middle + delta_x_pick_plate:
                motion_proxy.moveToward(0.5, 0, -0.03, lower_steps)
                print 'Toward'
            elif center_x > x_middle + delta_x_pick_plate:
                motion_proxy.moveToward(0, -0.5, 0, lower_steps)
                print 'Right'
            elif center_x < x_middle - delta_x_pick_plate:
                motion_proxy.moveToward(0, 0.5, 0, lower_steps)
                print 'Left'

        if i % 200 == 0:
            motion_proxy.moveToward(0, 0, 0)
    motion_proxy.moveToward(0, 0, 0)
    # 修正微调
    if center_down_y > y_close_too_much:  # 后退
        motion_proxy.moveTo(-0.05, 0, 0, smallTurnStep)
    if center_x < x_middle - delta_x_pick_plate:  # 向左跨
        motion_proxy.moveTo(0, 0.05, 0, smallTurnStep)
    motion_proxy.moveToward(0, 0, 0)

    motion_proxy.moveTo(0, 0.18, 0, smallTurnStep)  # 往左移
    print 'one step left'

    motion_proxy.moveTo(0.14, 0, 0, smallTurnStep)  # 前进一大步, 好大一步!
    print 'one step closer, 好大一步!'


    motion_proxy.moveTo(-0.05, 0, 0, smallTurnStep)  # 后退一小步

