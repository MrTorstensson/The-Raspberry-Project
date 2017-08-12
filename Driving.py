# Write Driver description here
# By Hannes

import Motor

class Tank:
    """ Description of driver """
    def __init__(self, Right = [11, 12], Left = [15,16]):
        """ Description of init, add everything thet needs to be set up """
        self.RightMotor = Motor.TankMotor(Right)
        self.LeftMotor = Motor.TankMotor(Left)

    def Move(self, speed, steer): # Funktioner du vill ha med
        self.RightMotor.SPEED(max(min(100, speed-steer), -100))
        self.LeftMotor.SPEED(max(min(100, speed+steer), -100))
        return True

    def close(self):
        """ Cleanup functions """
        self.RightMotor.close()
        self.LeftMotor.close()
