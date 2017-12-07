import RPi.GPIO as GPIO


def set_gpio_mode():
    # set GPIO warnings as false
    GPIO.setwarnings(False)
    # set up GPIO mode as BOARD
    GPIO.setmode(GPIO.BOARD)
