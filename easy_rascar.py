# 2017.10.26
# Author : c0sm0s (Yun Hyeok Kwak)
# Purpose : Control The Raspberry Car!!!!
#
# 이 모듈을 import한 후 RasCar 인스턴스를 생성하여 사용하세요

import time

import RPi.GPIO as GPIO


def set_motor_gpio_mode():
    # set GPIO warnings as false
    GPIO.setwarnings(False)
    # set up GPIO mode as BOARD
    GPIO.setmode(GPIO.BOARD)


class Motor:
    def __init__(self, pos, line_status=0):
        """
        Motor Class
        
        :param pos: 
        the position of motor
        
        :param line_status:
        Case 1: When you give pos L 
            If you give line_status 0, It sets line A to 12 and line B to 11
            If line_status 1, line A to 11 and line B to 12
        Case 2: When you give pos R
            If you give line_status 0, It sets line A to 15 and line B to 13
            If line_status 1, line A to 13 and line B to 15
        """
        # Check argument
        if not (pos == "L" or pos == "R"):
            raise Exception("please put 'L' or 'R' to pos argument")
        if not (line_status == 0 or line_status == 1):
            raise Exception("please put 0 or 1 to pos argument")

        def set_motor_gpio(_a, _b, _pwm):
            self._A = _a
            self._B = _b
            self._PWM = _pwm
            GPIO.setup(self._A, GPIO.OUT)
            GPIO.setup(self._B, GPIO.OUT)
            GPIO.setup(self._PWM, GPIO.OUT)
            self.PWM = GPIO.PWM(self._PWM, 100)
            self.PWM.start(0)

        if pos == "L":
            if line_status == 0:
                set_motor_gpio(12, 11, 35)
            elif line_status == 1:
                set_motor_gpio(11, 12, 35)

        elif pos == "R":
            if line_status == 0:
                set_motor_gpio(13, 15, 37)
            elif line_status == 1:
                set_motor_gpio(15, 13, 37)

    def run(self, direction, speed):
        """
        Make motor run
        :param direction: Forward or Backward as String
        :param speed: running speed
        """
        if not (direction == "F" or "B"):
            raise Exception("run method's direction must be 'F' or 'B'")
        if direction == "F":
            GPIO.output(self._A, GPIO.HIGH)
            GPIO.output(self._B, GPIO.LOW)
        elif direction == "B":
            GPIO.output(self._A, GPIO.LOW)
            GPIO.output(self._B, GPIO.HIGH)
        GPIO.output(self._PWM, GPIO.HIGH)
        self.PWM.ChangeDutyCycle(speed)

    def perfect_stop(self):
        GPIO.output(self._A, GPIO.LOW)
        GPIO.output(self._B, GPIO.LOW)
        GPIO.output(self._PWM, GPIO.LOW)
        self.PWM.ChangeDutyCycle(0)


class UltraSonicSensor:
    def __init__(self, trig=33, echo=31):
        self.trig = trig
        self.echo = echo
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def get_distance(self):
        #GPIO.output(self.trig, False)
        #time.sleep(0.5)
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)
        while GPIO.input(self.echo) == 0:
            pulse_start = time.time()
        while GPIO.input(self.echo) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)
        return distance


class TrackingSensor:
    """
    five way tracking sensor
    """

    def __init__(self, gpio_port=(16, 18, 22, 40, 32)):
        self.left_most_led = gpio_port[0]
        self.left_less_led = gpio_port[1]
        self.center_led = gpio_port[2]
        self.right_less_led = gpio_port[3]
        self.right_most_led = gpio_port[4]
        GPIO.setup(self.left_most_led, GPIO.IN)
        GPIO.setup(self.left_less_led, GPIO.IN)
        GPIO.setup(self.center_led, GPIO.IN)
        GPIO.setup(self.right_less_led, GPIO.IN)
        GPIO.setup(self.right_most_led, GPIO.IN)

    def scan(self):
        return_list = [self.left_most_led, self.left_less_led, self.center_led, self.right_less_led,
                       self.right_most_led]
        return [GPIO.input(x) for x in return_list]


class RasCar:
    def __init__(self):
        set_motor_gpio_mode()
        self.dat_file_name = "RasCar.txt"
        try:
            file_obj = open(self.dat_file_name, "r")

        # If a setting file doesn't exist, create the setting file and exit.
        except FileNotFoundError:
            file_obj = open(self.dat_file_name, "w")
            print("Setting File {0} Not Found. I created file just now. Please set {0}".format(self.dat_file_name))
            # 길어서 가독성을 위해 두줄로 나눈거... 사실 한줄이랑 효과 같음
            file_str = "Point_Power:\nPoint_L:\nPoint_R:\nSwing_Power:\nSwing_L:\nSwing_R:\n" \
                       "Curve_Power:\nCurve_Power_Plus:\nCurve_L:\nCurve_R:\nLine_Status_L:\nLine_Status_R:"
            file_obj.write(file_str)
            file_obj.close()
            exit()

        # If a setting file exist, parse the file
        self.setting = {}  # setting dictionary
        lines_list = file_obj.readlines()
        for i in lines_list:
            key, value = i.split(":")
            self.setting.update({key: float(value)})

        # Declare and initialize motor objects from saved Line_Status
        self.leftMotor = Motor("L", self.setting["Line_Status_L"])
        self.rightMotor = Motor("R", self.setting["Line_Status_R"])
        # Assign a UltraSonicSensor Object
        self.ultraSonicSensor = UltraSonicSensor()
        # Assign a TrackingSensor Object
        self.trackingSensor = TrackingSensor()

    def stop(self):
        self.leftMotor.perfect_stop()
        self.rightMotor.perfect_stop()

    def run(self, direction, speed, running_time=-1):
        """
        :param direction: "F" or "B". F means Forward, B means Backward
        :param speed: a integer [0,100]
        :param running_time: a integer >= 0
        You might pass running_time or not.
        If you do not pass running_time, Motors run forever until meets with another script
        """

        # Check argument
        if not (direction == "F" or direction == "B"):
            raise Exception("Please put 'F' or 'B' to direction")

        self.leftMotor.run(direction, speed)
        self.rightMotor.run(direction, speed)
        if not running_time == -1:
            time.sleep(running_time)
            self.stop()

    def swing_turn(self, direction):
        # Check argument
        if not (direction == "L" or direction == "R"):
            raise Exception("Please put 'L' or 'R' to direction")

        power = self.setting["Swing_Power"]
        if direction == "L":
            self.rightMotor.perfect_stop()
            self.leftMotor.run("B", power)
            running_time = self.setting["Swing_L"]
        elif direction == "R":
            self.leftMotor.perfect_stop()
            self.rightMotor.run("B", power)
            running_time = self.setting["Swing_R"]
        if not running_time == -1:
            time.sleep(running_time)
            self.stop()

    def point_turn(self, direction):
        # Check argument
        if not (direction == "L" or direction == "R"):
            raise Exception("Please put 'L' or 'R' to direction")

        power = self.setting["Point_Power"]
        if direction == "L":
            self.leftMotor.run("B", power)
            self.rightMotor.run("F", power)
            running_time = self.setting["Point_L"]
        elif direction == "R":
            self.leftMotor.run("F", power)
            self.rightMotor.run("B", power)
            running_time = self.setting["Point_R"]

        if not running_time == -1:
            time.sleep(running_time)
            self.stop()

    def curve_turn(self, direction):
        # Check argument
        if not (direction == "L" or direction == "R"):
            raise Exception("Please put 'L' or 'R' to direction")

        power = self.setting["Curve_Power"]
        power_plus = self.setting["Curve_Power_Plus"]
        if direction == "L":
            self.leftMotor.run("F", power)
            self.rightMotor.run("F", power + power_plus)
            running_time = self.setting["Curve_L"]
        elif direction == "R":
            self.leftMotor.run("F", power + power_plus)
            self.rightMotor.run("F", power)
            running_time = self.setting["Curve_R"]

        if not running_time == -1:
            time.sleep(running_time)
            self.stop()

    def curve_turn2(self, direction):
        # Check argument
        if not (direction == "L" or direction == "R"):
            raise Exception("Please put 'L' or 'R' to direction")

        power = self.setting["Curve_Power"]
        power_plus = self.setting["Curve_Power_Plus"] * 2
        if direction == "L":
            self.leftMotor.run("F", power)
            self.rightMotor.run("F", power + power_plus)
            running_time = self.setting["Curve_L"]
        elif direction == "R":
            self.leftMotor.run("F", power + power_plus)
            self.rightMotor.run("F", power)
            running_time = self.setting["Curve_R"]

        if not running_time == -1:
            time.sleep(running_time)
            self.stop()

