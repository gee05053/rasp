######################################################################
### Date: 2017/10/5
### file name: project3_student.py
### Purpose: this code has been generated for the three-wheeled moving
###         object to perform the project3 with ultra sensor
###         swing turn, and point turn
### this code is used for the student only
######################################################################

# =======================================================================
# import GPIO library and time module
# =======================================================================
import RPi.GPIO as GPIO
from time import sleep

# =======================================================================
#  set GPIO warnings as false
# =======================================================================
GPIO.setwarnings(False)

# =======================================================================
# import getDistance() method in the ultraModule
# =======================================================================
from ultraModule import *

# =======================================================================
# import TurnModule() method
# =======================================================================
from TurnModule import *


# =======================================================================
# rightPointTurn() and leftPointTurn() in TurnModule module
# =======================================================================
# student assignment (1)
# student assignment (2)

# =======================================================================
# import trackingModule() method
# =======================================================================
from trackingModule import *


# =======================================================================
# import go_forward_any(), go_backward_any(), stop(), LeftPwm(),
# RightPwm(), pwm_setup(), and pwm_low() methods in the module of go_any
# =======================================================================
from go_any import *

# implement rightmotor(x)  # student assignment (3)
# implement go_forward_any(speed): # student assignment (4)
# implement go_backward_any(speed): # student assignment (5)
# implement go_forward(speed, running_time)  # student assignment (6)
# implement go_backward(speed, running_time)  # student assignment (7)

# =======================================================================
# setup and initilaize the left motor and right motor
# =======================================================================
pwm_setup()

# =======================================================================
#  define your variables and find out each value of variables
#  to perform the project3 with ultra sensor
#  and swing turn
# =======================================================================
dis = 20  # 장애물과의 거리
obstacle = 1

# when obstacle=1, the power and
# running time of the first turn
curvePr = 25
curveTr = 0.2

try:
    while True:
        get_tracking = scan() #get tracking list ex) [1,1,1,1,1], [0,0,0,0,0]
        get_distance = getDistance()
        print("Distance =", get_distance)
        if get_distance >= dis :
            if get_tracking == [0,1,1,1,1] or [0,0,1,1,1]:
                leftCurveTurn(curvePr+10, curveTr)
            elif get_tracking == [1,0,1,1,1] :
                leftCurveTurn(curvePr, curveTr)
            elif get_tracking == [1,1,1,0,1] :
                rightCurveTurn(curvePr, curveTr)
            elif get_tracking == [1,1,1,1,0] or [1,1,1,0,0] :
                rightCurveTurn(curvePr+10, curveTr)
            elif get_tracking == [0,0,0,0,0] :
                stop()
                sleep(1)
                break
            else :
                go_forward_any(35)
            print("Obstacle =",obstacle)
        else :
            rightCurveTurn(curvePr+30, curveTr+0.5)
            stop()
            sleep(1)
            go_forward(35, 1)
            leftCurveTurn(curvePr+30, curveTr+0.5)
            stop()
            sleep(1)
            go_forward(35, 1)
            leftCurveTurn(curvePr+10, curveTr+0.3)
            go_forward(35,2)
            obstacle += 1
            continue


            ########################################################
            ### please continue the code or change the above code
            ### # student assignment (10)
            ########################################################


# when the Ctrl+C key has been pressed,
# the moving object will be stopped

except KeyboardInterrupt:
    pwm_low()
