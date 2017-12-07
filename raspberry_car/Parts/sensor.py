import RPi.GPIO as GPIO
import time


class TrackingSensor:
    """
    five way tracking sensor
    """

    def __init__(self, gpio_port=(16, 18, 22, 40, 32)):
        # ports sequence : Left -> Right
        self.portsOfSensor = gpio_port
        for port in self.portsOfSensor:
            GPIO.setup(port, GPIO.IN)

    def scan(self):
        return [GPIO.input(port) for port in self.portsOfSensor]


class UltraSonicSensor:
    """
    Ultra sonic sensor
    """
    def __init__(self, trig=33, echo=31):
        self.trig = trig
        self.echo = echo
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def get_distance(self):
        GPIO.output(self.trig, False)
        time.sleep(0.05)
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
