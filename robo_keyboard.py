from robot import Otto
from numpy import pi
import numpy as np

from constants import A_PUNTA


def touch_key(key: list, robot: Otto):
    robot.move_j(key, 400)
    robot.move_l([0, 0, -1], 50, speed=400)
    robot.move_l([0, 0, 1], 50, speed=400)


def write_keyboard(phrase: str, r_otto, letters_coord):
    for l in phrase:
        touch_key(letters_coord[l], r_otto)


letters = {
    "i": [10, -150, 70],
    "q": [10 - 125, -150 - 5, 65],
    "u": [-10, -150, 70],
    "a": [-115 + 5, -155 - 20, 65],
    "l": [10 + 25, -150 - 20, 70],
    "n": [35 - 45, -170 - 20, 65],
    ".": [35 + 5, -170 - 20, 67],
    "e": [-115 + 40, -155, 67],
    "t": [-115 + 75, -153, 67],
    "enter": [35+70, -153, 67]
}

otto = Otto(program_name="keyboard.gcode", custom_tool=A_PUNTA)
# otto.move_j(letters["q"], speed=400)
# otto.move_l([0, 0, -1], 40, speed=400)


write_keyboard("iquall.net", otto, letters)
touch_key(letters["enter"], otto)

# touch_key(letters["i"], otto)
# touch_key(letters["q"], otto)
# touch_key(letters["u"], otto)
# touch_key(letters["a"], otto)
# touch_key(letters["l"], otto)
# touch_key(letters["l"], otto)

# otto.gen_abs_move_gcode(a, 400)
# otto.gen_abs_move_gcode(b, 200)
# otto.gen_abs_move_gcode(c, 200)
