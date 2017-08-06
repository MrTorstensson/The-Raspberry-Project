# This is a small motor driver intended to be used on a raspberry pi
# Added to GIT by MrTorstensson
# Feel free to use/reuse

import RPi.GPIO as GPIO

class Motor:
    """ Will set up a PWM motor control """
    def __init__(self, PORT = [11, 13]):
        """__init__(self, PORT = [11, 13]), Will set up a PWM motor control on PORT = [11, 13] """
        self.FWD = PORT[0]
        self.REW = PORT[1]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.FWD, GPIO.OUT)
        GPIO.setup(self.REW, GPIO.OUT)
        self.fwd = GPIO.PWM(self.FWD, 100)
        self.rew = GPIO.PWM(self.REW, 100)
        self.fwd.start(0)
        self.rew.start(0)
        
    def SPEED(self, Throttle):
        """SPEED(self, Throttle), Input float will set the Motor in a -100% to 100% speed range """
        if Throttle < 0:
            self.fwd.ChangeDutyCycle(0)
            self.rew.ChangeDutyCycle(-Throttle)
        else:
            self.fwd.ChangeDutyCycle(Throttle)
            self.rew.ChangeDutyCycle(0)

    def close(self):
        """ House keeping cleanup of GPIO ports, when motor is released """
        GPIO.cleanup([self.FWD, self.REW])
        
