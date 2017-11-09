import RPi.GPIO as GPIOA

def scan():
    self.left_most_led = 16
    self.left_less_led = 18
    self.center_led = 22
    self.right_less_led = 40
    self.right_most_led = 32
    GPIO.setup(self.left_most_led, GPIO.IN)
    GPIO.setup(self.left_less_led, GPIO.IN)
    GPIO.setup(self.center_led, GPIO.IN)
    GPIO.setup(self.right_less_led, GPIO.IN)
    GPIO.setup(self.right_most_led, GPIO.IN)
    return_list = [self.left_most_led, self.left_less_led, self.center_led, self.right_less_led, self.right_most_led]
    return [str(GPIO.input(x)) for x in return_list]