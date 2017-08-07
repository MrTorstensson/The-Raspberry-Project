#Importing
import RPi.GPIO as GPIO
import time

class Bat:
    #initiate
    def __init__(self, PORT = [15, 16]):
        """__init__(self, PORT = [15, 16]), i setting up Ultrasonic reader on ports 15, 16"""
        self.Trigger_port = PORT[0]
        self.Echo_port = PORT[1]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.Trigger_port, GPIO.OUT)
        GPIO.setup(self.Echo_port, GPIO.IN)

    def distance(self):
        """distance(self), Returning a single reading """ 
        #Trigger Pulse
        GPIO.output(self.Trigger_port, True)
        time.sleep(0.00001)
        GPIO.output(self.Trigger_port, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime and watch for trigger error (0.1s timeout).
        while GPIO.input(self.Echo_port) == 0 and StopTime + 0.1 > StartTime:
            StartTime = time.time()
        # save time of arrival
        while GPIO.input(self.Echo_port) == 1:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        if TimeElapsed < 0:
            return False
        # multiply with the sonic speed (343 m/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 343) / 2
        # if measurment is larger then 5.
        if distance > 5:
            return False
        return distance

    def measure(self, sample = 10, remove = 3):
        """ measure(self, sample = 10, remove = 3), method where "sample" samples are collected and the "remove" highest and lowest are deleted.
        return valu is the mean of the remaining samples"""
        Values = []
        while len(Values) < sample:
            Values.append(self.distance())
        Values.sort()
        Select = Values[remove:-remove]
        return sum(Select)/len(Select)

    def Test(self, Time = 10):
        Values = []
        StartTime = time.time()
        while time.time() < (StartTime + Time):
            Values.append(self.distance())
        return("%s measurements within %s seconds. Average rate  %s Hz" %(len(Values), Time, len(Values)/Time))

    def close(self):
        GPIO.cleanup([self.Trigger_port, self.Echo_port])
        print("GPIO.cleanup([%s, %s])" % (self.Trigger_port, self.Echo_port))
