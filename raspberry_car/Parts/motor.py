import RPi.GPIO as GPIO


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
            GPIO.output(self._PWM, GPIO.HIGH)

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
        self.PWM.ChangeDutyCycle(speed)

    def stop(self):
        self.PWM.ChangeDutyCycle(0)

    def perfect_stop(self):
        """
        If you want to stop for a moment, Do not use this.
        Instead of this, Use stop method
        """
        GPIO.output(self._PWM, GPIO.LOW)
        self.PWM.ChangeDutyCycle(0)


class MotorTest(Motor):
    def __del__(self):
        self.perfect_stop()
