DEBUG = False

################
##### AXIS #####
################

MOTOR_ANLGLE_PER_STEP = [1.8, 1.8, 1.8]  # Angulo en grados

MOTOR_MICROSTEP_REDUCTION = [1, 1, 1]  # Microsteps 1- 1/2 - 1/4 - 1/16 ...

MOTOR_REDUCTION = [20 / 252, 16 / 252, 20 / 80]  # Motor 0,1,2

##################
##### CONFIG #####
##################
MOTOR_STEPS_PER_MM_CONFIG = [200, 20, 20]

DEG_TO_GRBL = [1 / (MOTOR_ANLGLE_PER_STEP[i] * MOTOR_REDUCTION[i] * MOTOR_STEPS_PER_MM_CONFIG[i]) for i in range(3)]

################
#### GCODE #####
################


INIT_INSTRUCTIONS = '''$X ; Unlocking Robot
$H ; Homming cycle
'''

ABS_MOVE_CMD = "G90"
REL_MOVE_CMD = "G91"
GCODE_MOVE_TEMPLATE = "G21{mode}X{axis_2:.2f}Y{axis_1:.2f}Z{axis_0:.2f}F{speed}"

MOOVE_L_STEP = 1 # En milimetros mm

################
#### OTTO #####
################

ARM_1_LEN = 200  # Largo en mm
ARM_2_LEN = 200  # Largo en mm

A_BASE = [[1, 0, 0, 105.5],
          [0, 1, 0, 95.7],
          [0, 0, 1, 224],
          [0, 0, 0, 1]]
A_TOOL = [[1, 0, 0, 0],
          [0, 1, 0, -30],
          [0, 0, 1, -20],
          [0, 0, 0, 1]]

#######################
#### CUSTOM TOOLS #####
#######################


A_FIBRON = [[1, 0, 0, -31],
      [0, 1, 0, 0],
      [0, 0, 1, -3],
      [0, 0, 0, 1]]

A_PUNTA = [[1, 0, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 1, -5],
      [0, 0, 0, 1]]