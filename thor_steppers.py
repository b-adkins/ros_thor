#!/usr/bin/env python

## Hello world! Tells A4988 to turn stepper motor at constant velocity.

import sys
import time

import RPi.GPIO as GPIO

#
# Pin configuration
#


GPIO.setmode(GPIO.BOARD)

# Enable
GPIO.setup(5, GPIO.OUT, initial=True)
GPIO.setup(10, GPIO.OUT, initial=True)

# Step
GPIO.setup(7, GPIO.OUT, initial=False)
GPIO.setup(11, GPIO.OUT, initial=False)

# Dir
GPIO.setup(8, GPIO.OUT, initial=False)
GPIO.setup(12, GPIO.OUT, initial=True)

def enable():
    '''
    Sets ENABLE pin so A4988s move
    '''
    GPIO.output(5, False)
    GPIO.output(10, False)

def disable():
    '''
    '''
    GPIO.output(5, True)
    GPIO.output(10, True)


enable()

if len(sys.argv) > 1:
    if sys.argv[1] == "yaw":
        GPIO.output(8, True)
        GPIO.output(12, True)
    elif sys.argv[1] == "-yaw":
        GPIO.output(8, False)
        GPIO.output(12, False)

while(True):
    GPIO.output(7, True)
    GPIO.output(11, True)
    time.sleep(1e-5)
    GPIO.output(7, False)
    GPIO.output(11, False)
    time.sleep(3e-2)
