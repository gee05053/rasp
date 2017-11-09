import RPi.GPIO as GPIOA

def scan():
    left_most_led = 16
    left_less_led = 18
    center_led = 22
    right_less_led = 40
    right_most_led = 32
    GPIO.setup(left_most_led, GPIO.IN)
    GPIO.setup(left_less_led, GPIO.IN)
    GPIO.setup(center_led, GPIO.IN)
    GPIO.setup(right_less_led, GPIO.IN)
    GPIO.setup(right_most_led, GPIO.IN)
    return_list = [left_most_led, left_less_led, center_led, right_less_led, right_most_led]
    return [str(GPIO.input(x)) for x in return_list]