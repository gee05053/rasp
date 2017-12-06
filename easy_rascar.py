# since 2017.10.26
# version. 2
# Author : c0sm0s (Yun Hyeok Kwak)
# Purpose : Control The Raspberry Car!!!!
#
# 이 모듈을 import한 후 원하는 RasCar 인스턴스를 생성하여 사용하세요

import time
from Parts.mode import set_gpio_mode
from Parts.motor import Motor
from Parts.sensor import TrackingSensor
import RPi.GPIO as GPIO


class RasCar:
    def __init__(self, line_status_of_left_motor, line_status_of_right_motor):
        set_gpio_mode()

        # Declare and initialize motor objects from line_Statuses
        self.leftMotor = Motor("L", line_status_of_left_motor)
        self.rightMotor = Motor("R", line_status_of_right_motor)

    def __del__(self):
        self.leftMotor.perfect_stop()
        self.rightMotor.perfect_stop()
        GPIO.cleanup()

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()

    def run(self, direction, speed, running_time=-1):
        """
        :param direction: 'F' or 'B'. F means 'F'orward, B means 'B'ackward
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

    def swing_turn(self, direction, power, running_time=-1):
        # Check argument
        if not (direction == "L" or direction == "R"):
            raise Exception("Please put 'L' or 'R' to direction")

        if direction == "L":
            self.leftMotor.stop()
            self.rightMotor.run("F", power)
        elif direction == "R":
            self.rightMotor.stop()
            self.leftMotor.run("F", power)

        if not running_time == -1:
            time.sleep(running_time)
            self.stop()

    def point_turn(self, direction, power, running_time=-1):
        # Check argument
        if not (direction == "L" or direction == "R"):
            raise Exception("Please put 'L' or 'R' to direction")

        if direction == "L":
            self.leftMotor.run("B", power)
            self.rightMotor.run("F", power)
        elif direction == "R":
            self.leftMotor.run("F", power)
            self.rightMotor.run("B", power)

        if not running_time == -1:
            time.sleep(running_time)
            self.stop()

    def curve_turn(self, direction, power, power_plus, running_time=-1):
        # Check argument
        if not (direction == "L" or direction == "R"):
            raise Exception("Please put 'L' or 'R' to direction")

        if direction == "L":
            self.leftMotor.run("F", power)
            self.rightMotor.run("F", power + power_plus)
        elif direction == "R":
            self.leftMotor.run("F", power + power_plus)
            self.rightMotor.run("F", power)

        if not running_time == -1:
            time.sleep(running_time)
            self.stop()


class RasCarUsingTrackingSensor(RasCar):
    def __init__(self, line_status_of_left_motor, line_status_of_right_motor):
        super(RasCarUsingTrackingSensor, self).__init__(line_status_of_left_motor, line_status_of_right_motor)
        # Assign a TrackingSensor Object
        self.trackingSensor = TrackingSensor()
