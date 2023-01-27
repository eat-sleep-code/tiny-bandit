import pygame
import RPi.GPIO as GPIO


def initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #BUTTON 1 (LEFT)
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #BUTTON 2 (RIGHT)
    GPIO.setup(26, GPIO.OUT) #3V OUT
    GPIO.setup(27, GPIO.OUT) #LED

    GPIO.output(26, GPIO.HIGH) #Set to always deliver 3V



def isButtonPressed(side):
    if side == "right":
        pin = 11
    else: 
        pin = 10

    if GPIO.input(pin) == GPIO.HIGH:
        return True
    else:
        return False



def blinkLED(times = 20, delay = 100):
    for i in range(0, times):
        GPIO.output(27, GPIO.HIGH)
        pygame.time.delay(delay)
        GPIO.output(27, GPIO.LOW)



def cleanup():
    GPIO.cleanup()