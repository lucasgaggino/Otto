import numpy as np
from math import pi, sin, cos, atan2, acos
import math

from constants import *


class Otto:
    init_angle_offset = np.array([np.radians(-70), np.radians(3), np.radians(-13)])  # [theta0,theta1,theta2]
    home = np.array([0, pi / 4, 0])
    gcode_file = ""
    q = np.array([0, 0, 0])
    a_base = np.array(A_BASE)
    a_tool = np.array(A_TOOL)
    a_tool_custom = np.eye(4)
    last_coord= np.array([0,0,0])

    def __init__(self, program_name: str = "Otto.gcode", custom_tool: np.array = np.eye(4)):
        self.gcode_file = program_name
        self.a_tool_custom = custom_tool
        print(f"Creating gcode file with name: {program_name}")
        with open(program_name, 'w') as f:
            f.write(INIT_INSTRUCTIONS)
            f.close()
        self.gen_abs_move_gcode(self.home, 400)
        self.last_coord = self.d_kinematics(self.home)

    def __del__(self):
        # self.gen_abs_move_gcode(self.home, 400)
        print("Ending Gcode file, Sending Otto Home")

    def gen_abs_move_gcode(self, q: np.array, speed: int):
        self.q = q
        if DEBUG:
            print(q / pi)
            a = self.d_kinematics(q)
            # print(a)
            qi = self.i_kinematics(a)
            print(qi / pi)
            print("----------")
        q = q - self.init_angle_offset
        q = np.degrees(q) * DEG_TO_GRBL
        command = GCODE_MOVE_TEMPLATE.format(mode=ABS_MOVE_CMD,
                                             axis_0=q[0],
                                             axis_1=q[1],
                                             axis_2=q[2],
                                             speed=speed)

        with open(self.gcode_file, 'a') as f:
            f.write(command + '\n')
            f.close()

    def gen_rel_move_gcode(self, q, speed) -> None:
        self.q = self.q + q
        q = np.degrees(q) * DEG_TO_GRBL
        command = GCODE_MOVE_TEMPLATE.format(mode=REL_MOVE_CMD,
                                             axis_0=q[0],
                                             axis_1=q[1],
                                             axis_2=q[2],
                                             speed=speed)

        with open(self.gcode_file, 'a') as f:
            f.write(command + '\n')
            f.close()

    def d_kinematics(self, q) -> np.array:
        pose = np.eye(4)

        d_len = ARM_1_LEN * sin(q[1]) + ARM_2_LEN * cos(q[2] - q[1])
        d_height = ARM_1_LEN * cos(q[1]) + ARM_2_LEN * sin(q[2] - q[1])
        pose[0, 3] = d_len * sin(q[0])
        pose[1, 3] = d_len * -cos(q[0])
        pose[2, 3] = d_height

        pose[0, 0] = cos(q[0])
        pose[0, 1] = -sin(q[0])
        pose[1, 0] = sin(q[0])
        pose[1, 1] = cos(q[0])

        return self.a_base.dot(pose).dot(self.a_tool).dot(self.a_tool_custom)

    def i_kinematics(self, pose_final, config=1) -> np.array:
        # La configuracion solo considera Codo arriba o abajo, dado que es la unica mecanicamente posible
        q = np.zeros(3)
        a = np.linalg.inv(self.a_base).dot(pose_final).dot(np.linalg.inv(self.a_tool.dot(self.a_tool_custom)))

        q[0] = atan2(a[1, 3], a[0, 3])  # No se considera el brazo atras por topes mecanicos
        s0 = sin(q[0])
        c0 = cos(q[0])

        dist = np.sqrt(a[1, 3] ** 2 + a[0, 3] ** 2)
        height = a[2, 3]
        arm_len = [ARM_1_LEN, ARM_2_LEN]

        if config == 1:
            q[2] = -acos((height ** 2 + dist ** 2 - arm_len[0] ** 2 - arm_len[1] ** 2) / (2 * arm_len[0] * arm_len[1]))
            q[1] = atan2(height, dist) - atan2(arm_len[1] * sin(q[2]), arm_len[0] + arm_len[1] * cos(q[2]))
        else:
            q[2] = acos((height ** 2 + dist ** 2 - arm_len[0] ** 2 - arm_len[1] ** 2) / (2 * arm_len[0] * arm_len[1]))
            q[1] = atan2(height, dist) - atan2(arm_len[1] * sin(q[2]), arm_len[0] + arm_len[1] * cos(q[2]))

        q[0] = q[0] + pi / 2
        q[1] = -q[1] + pi / 2
        q[2] = q[2] + pi / 2

        return q

    def move_j(self, coord, speed=200):
        coord = np.array(coord)
        a = self.pose_to_a(coord)
        q = self.i_kinematics(a)
        self.gen_abs_move_gcode(q, speed)
        self.last_coord = coord

    def move_l(self, direction, length, speed=200):

        direction = np.array(direction)
        init_coord = self.last_coord

        steps = np.linspace(0, 1, num=int(length / MOOVE_L_STEP))
        for step in steps[2:]:
            new_coord = init_coord + direction*step*length
            #print(f"MOVE_L:{new_coord}")
            self.move_j(new_coord, speed=speed)

    def pose_to_a(self, coord):
        # coord = [X,Y,Z]
        a = np.eye(4)
        a[0, 3] = coord[0]
        a[1, 3] = coord[1]
        a[2, 3] = coord[2]

        return a
