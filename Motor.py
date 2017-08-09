# This is a small motor driver intended to be used on a raspberry pi
# Added to GIT by MrTorstensson
# Feel free to use/reuse

import RPi.GPIO as GPIO

class Motor:
    """ Will set up a PWM motor control """
    def __init__(self, PORT = [7, 8], Limit = 40):
        """__init__(self, PORT = [11, 13]), Will set up a PWM motor control on PORT = [11, 13] """
        """ The limit added is the minimum pulsewidth that will be used on the motor, in order to avoid noize at low power """
        self.FWD = PORT[0]
        self.REW = PORT[1]
        self.Limit = Limit
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.FWD, GPIO.OUT)
        GPIO.setup(self.REW, GPIO.OUT)
        self.fwd = GPIO.PWM(self.FWD, 100)
        self.rew = GPIO.PWM(self.REW, 100)
        self.fwd.start(0)
        self.rew.start(0)
        
    def SPEED(self, Throttle):
        """SPEED(self, Throttle), Input float will set the Motor in a -100% to 100% speed range """
        if abs(Throttle) < self.Limit:
            if(Throttle > 0):
                self.fwd.ChangeFrequency(1./((100-self.Limit)*self.Limit/Throttle+self.Limit)*10000)
                self.fwd.ChangeDutyCycle(self.Limit)
                self.rew.ChangeDutyCycle(0)
            elif(Throttle < 0):
                self.rew.ChangeFrequency(1./((100-self.Limit)*self.Limit/-Throttle+self.Limit)*10000)
                self.fwd.ChangeDutyCycle(0)
                self.rew.ChangeDutyCycle(self.Limit)
            else:
                self.fwd.ChangeDutyCycle(0)
                self.rew.ChangeDutyCycle(0)
        elif Throttle < 0:
            self.rew.ChangeFrequency(100)
            self.fwd.ChangeDutyCycle(0)
            self.rew.ChangeDutyCycle(-Throttle)
        else:
            self.fwd.ChangeFrequency(100)
            self.fwd.ChangeDutyCycle(Throttle)
            self.rew.ChangeDutyCycle(0)

    def close(self):
        """ House keeping cleanup of GPIO ports, when motor is released """
        GPIO.cleanup([self.FWD, self.REW])
        
