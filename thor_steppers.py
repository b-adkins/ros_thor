#!/usr/bin/env python

## Crude high level stepper motor controllers

import os.path
import sys
import time

import RPi.GPIO as GPIO


class Motor(object):
    ## My wiring uses yellow for dir, green for step, and blue for enable 
    def __init__(self, direction, step, enable):
        self._direction_pin = direction
        self._step_pin = step
        self._enable_pin = enable

        self._direction = False
        
        GPIO.setup(self._direction_pin, GPIO.OUT, initial=self._direction)
        GPIO.setup(self._step_pin, GPIO.OUT, initial=False)
        GPIO.setup(self._enable_pin, GPIO.OUT, initial=True)        

    def enable(self):
        '''
        Sets ENABLE pin so A4988s moves.
        '''
        GPIO.output(self._enable_pin, False)

    def disable(self):
        '''
        Sets ENABLE pin so A4988s goes limp.
        '''
        GPIO.output(self._enable_pin, True)

    @property
    def direction(self):
        return _direction

    @direction.setter
    def direction(self, direction):
        self._direction = direction
        GPIO.output(self._direction_pin, direction)

    def step(self):
        GPIO.output(self._step_pin, True)
        time.sleep(1e-5)
        GPIO.output(self._step_pin, False)
        
       
#
# Pin configuration
#

GPIO.setmode(GPIO.BOARD)


motors = {
#    "art1": Motor(36, 35, 33),
#    "art2a": Motor(32, 31, 29),
#    "art2b": Motor(24, 23, 26),
    "art1": Motor(32, 31, 29),
    "art2": Motor(24, 23, 26),
    "art3": Motor(22, 21, 19),
    "art4": Motor(16, 15, 13),
    "art5": Motor(8, 7, 5),
    "art6": Motor(12, 11, 10)
}

def usage(exe_name):
    print('''Usage: {} cmd

Valid commands: yaw, -yaw, roll, -roll, art4, art3, art2
    '''.format(exe_name))


# Simple default executable
if __name__ == "__main__":
    cmd = ""
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
    else:
        usage(os.path.basename(sys.argv[0]))
        sys.exit(2)


    for m in motors.values():
        m.disable()

        
    if cmd == "yaw":
        motors["art5"].direction = True
        motors["art6"].direction = True
        motors["art5"].enable()
        motors["art6"].enable()           
    elif cmd == "-yaw":
        motors["art5"].direction = False
        motors["art6"].direction = False
        motors["art5"].enable()
        motors["art6"].enable()
    elif cmd == "roll":
        motors["art5"].direction = True
        motors["art6"].direction = False
        motors["art5"].enable()
        motors["art6"].enable()
    elif cmd == "-roll":
        motors["art5"].direction = False
        motors["art6"].direction = True
        motors["art5"].enable()
        motors["art6"].enable()
    elif cmd == "art4":
        motors["art4"].direction = True
        motors["art4"].enable()
    elif cmd == "art3":
        motors["art3"].direction = True
        motors["art3"].enable()
    elif cmd == "art2":
        motors["art2"].direction = True
        motors["art2"].enable()
    elif cmd == "art1":
        motors["art1"].direction = True
        motors["art1"].enable()
    else:
        usage(os.path.basename(sys.argv[0]))
        sys.exit(2)
    
            
    try:
        while(True):
            for m in motors.values():
                m.step()
            time.sleep(3e-2)
            
    finally:
        for m in motors.values():
            m.disable()
        GPIO.cleanup()
