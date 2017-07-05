#!/usr/bin/env python

## Crude high level stepper motor controllers

import os.path
import readline
import sys
import thread
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


def disable_all():
    for m in motors.values():
        m.disable()

def enable_all():
    for m in motors.values():
        m.enable()

        
#
# Simple default executable
#


def usage(exe_name):
    print('''Usage: {}

Enters a motor shell
{}
'''.format(exe_name, shell_usage_msg()))

def shell_usage_msg():
    return '''Valid commands:
    yaw, -yaw, roll, -roll, art4, art3, art2, art1, -art4, -art3, -art2, -art1
    '''

def tick_thread():
    while(True):
        for m in motors.values():
            m.step()
            time.sleep(3e-3)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["help", '-h', "--help"]:
        usage(os.path.basename(sys.argv[0]))
        sys.exit(2)
 
    try:
        disable_all()
        cmd = ''
        thread.start_new_thread(tick_thread, ())
        
        while cmd not in ["q", "quit", "exit"]:
            cmd = raw_input("<o>: ")
            
            if cmd in ["help", "h"]:
                print(shell_usage_msg())
            elif cmd == "yaw":
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
            elif cmd == "-art4":
                motors["art4"].direction = False
                motors["art4"].enable()
            elif cmd == "-art3":
                motors["art3"].direction = False
                motors["art3"].enable()
            elif cmd == "-art2":
                motors["art2"].direction = False
                motors["art2"].enable()
            elif cmd == "-art1":
                motors["art1"].direction = False
                motors["art1"].enable()
            elif cmd in ["stop", 's']:
                for m in motors.values():
                    m.disable()   
                        
    finally:
        disable_all()
        GPIO.cleanup()
