#!/usr/bin/env python

## Hello world! Tells A4988 to turn stepper motor at constant velocity.

import time

import RPi.GPIO as GPIO

# Set up pins
GPIO.setmode(GPIO.BOARD)

# Enable
GPIO.setup(5, GPIO.OUT, initial=True)

# Step
GPIO.setup(7, GPIO.OUT, initial=False)

# Dir
GPIO.setup(8, GPIO.OUT)

def enable():
    '''
    Sets ENABLE pin so A4988s move
    '''
    GPIO.output(5, False)

def disable():
    '''
    '''
    GPIO.output(5, True)


enable()

while(True):
    GPIO.output(7, True)
    time.sleep(1e-5)
    GPIO.output(7, False)
    time.sleep(1e-2)
