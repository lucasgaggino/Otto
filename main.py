from robot import Otto
from numpy import pi
import numpy as np

from constants import A_FIBRON

a = np.array([0, -pi / 10, 0])
b = np.array([0, pi / 4, 0])
c = np.array([pi / 2, pi / 2, pi / 2])

speed = 100
otto = Otto(program_name="testRep.gcode",custom_tool=A_FIBRON)
otto.move_j([-150, -150, 10], speed=400)
otto.move_l([0, 1, 0], 200, speed=speed)
otto.move_l([0, -1, 0], 200, speed=speed)
otto.move_l([0, 1, 0], 200, speed=speed)
otto.move_l([0, -1, 0], 200, speed=speed)

# otto.gen_abs_move_gcode(a, 400)
# otto.gen_abs_move_gcode(b, 200)
# otto.gen_abs_move_gcode(c, 200)
