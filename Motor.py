# This is a small motor driver intended to be used on a raspberry pi
# Added to GIT by MrTorstensson
# Feel free to use/reuse

import RPi.GPIO as GPIO

class pwmMotor:
    """ Will set up a PWM motor control """
    def __init__(self, PORT = [11, 12], Limit = 40):
        """__init__(self, PORT = [11, 13]), Will set up a PWM motor control on PORT = [11, 13] """
        """ The limit added is the minimum pulsewidth that will be used on the motor, in order to avoid noize at low power """
        self.Limit = Limit
        self.PORT = PORT
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PORT[0], GPIO.OUT)
        GPIO.setup(PORT[1], GPIO.OUT)
        self.fwd = GPIO.PWM(PORT[0], 100)
        self.rew = GPIO.PWM(PORT[1], 100)
        self.fwd.start(0)
        self.rew.start(0)
        
    def SPEED(self, Throttle):
        """SPEED(self, Throttle), Input float will set the Motor in a -100% to 100% speed range """
        if abs(Throttle) < self.Limit:
            self.fwd.ChangeDutyCycle(0)
            self.rew.ChangeDutyCycle(0)
        elif Throttle < 0:
            self.fwd.ChangeDutyCycle(0)
            self.rew.ChangeDutyCycle(-Throttle)
        else:
            self.fwd.ChangeDutyCycle(Throttle)
            self.rew.ChangeDutyCycle(0)

    def close(self):
        """ House keeping cleanup of GPIO ports, when motor is released """
        self.fwd.stop()
        self.rew.stop()
        GPIO.cleanup(self.PORT)
        
class TankMotor:
    """ Will set up a PWM like motor control well suited for large motors to run slow but can have problem with rapid update < 0.5s """
    def __init__(self, PORT = [11, 12]):
        """__init__(self, PORT = [11, 13]), Will set up a PWM motor control on PORT = [11, 13] """
        """ The limit added is the minimum pulsewidth that will be used on the motor, in order to avoid noize at low power """
        self.PORT = PORT
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PORT[0], GPIO.OUT)
        GPIO.setup(PORT[1], GPIO.OUT)
        self.fwd = GPIO.PWM(PORT[0], 1)
        self.rew = GPIO.PWM(PORT[1], 1)
        self.fwd.start(0)
        self.rew.start(0)
        
    def SPEED(self, Throttle):
        """SPEED(self, Throttle), Input float will set the Motor in a -100% to 100% speed range """
        if Throttle < 0:
            self.rew.ChangeFrequency(max(1,abs(Throttle)))
            self.fwd.ChangeDutyCycle(0)
            self.rew.ChangeDutyCycle(min(100, -Throttle*2))
        else:
            self.fwd.ChangeFrequency(max(1,abs(Throttle)))
            self.fwd.ChangeDutyCycle(min(100, Throttle*2))
            self.rew.ChangeDutyCycle(0)

    def close(self):
        """ House keeping cleanup of GPIO ports, when motor is released """
        self.fwd.stop()
        self.rew.stop()
        GPIO.cleanup(self.PORT)
