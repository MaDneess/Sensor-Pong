import time, Commons

from StaticUtils import StaticUtils
from CommUtils import CommUtils
from CommController import CommController
from threading import Thread


class PressureDevice(Thread):
    
    def __init__(self, args, board):
        super().__init__()
        self.commCont = CommController(args)
        self.board = board
        self.MINIMUM = 0
        self.MAXIMUM = 1
        self.READING = 0
        self.started = StaticUtils.getMillis()


    """
        Description:
            Thread runnable method
    """
    def run(self):
        while self.board.state != Commons.EXIT:
            while self.isOpen() and self.board.state == Commons.IN_GAME:
                if (StaticUtils.getMillis() - self.started) > 350:
                    self.READING = self.getReadings(None, 1)
                    self.started = StaticUtils.getMillis()
        # close serial on exit
        self.close()

    """
        Description:
            Method takes 5 readings and sets minimum point 
    """
    def calibrateMin(self):
        self.MINIMUM = self.mean(self.getReadings([], 5))

    """
        Description:
            Method takes 5 readings and sets maximum point 
    """
    def calibrateMax(self):
        self.MAXIMUM = self.mean(self.getReadings([], 5))

    """
        Description:
            Method takes 100 reading from the device and calculates middle point
    """
    def calibrate(self):
        # prepare readings list
        readings = self.getReadings([], CommUtils.CALIBRATION_DATA_SIZE)
        # find regular mean
        reg_mean = self.mean(readings)
        # sort readings and find median value
        StaticUtils.mergeSort(readings, 0, len(readings)-1)
        median = self.median(readings)
        # format readings from extreme values and find trimmed mean
        readings = self.formatReadings(readings, int(CommUtils.CALIBRATION_DATA_SIZE*.2))
        trim_mean = self.mean(readings)
        
        self.DATA_MIDDLE_POINT = (reg_mean + median + trim_mean) / 3
        self.READING = self.DATA_MIDDLE_POINT
        
    """
        Description:
            Method find list mean (regular average value)
    """
    def mean(self, values):
        return sum(values) / len(values)
    
    """
        Description:
            Method finds median value of a given array
        :param {values}
            
    """
    def median(self,values):
        if len(values) % 2 == 0:
            mid = int((len(values)-1) /2)
            return (values[mid] + values[mid+1]) / 2
        else:
            return values[int(len(values) / 2)]
            
    """
        :param {values} - list of values
        :param {ran} - range of required values in the list
        Description:
            Method cuts values from a list in a specified range
        Return:
            temp[]
    """
    def formatReadings(self, values, ran):
        start = int(len(values)/2) - int(ran/2)
        end = int(len(values)/2) + int(ran/2)
        temp = []
        for i in range(start, end):
            temp.append(values[i])
        return temp
        
    """
        Description:
            Method gets string message from the comm controller
            and try parses it into float
    """
    def getReadings(self, readings, num):
        def get():
            temp = None
            while (temp is None) or (not temp[1]):
                temp = StaticUtils.floatTryParse( self.commCont.readBuffer() )
                if (temp is not None) and (temp[1]):
                    return round(temp[0], 2)
        if (readings is not None) and (num > 1):
            while len(readings) <= num:
                time.sleep(.3)
                readings.append(get())
            return readings
        elif (readings is None) and (num == 1):
            return get()
        else:
            raise ValueError("Invalid arguments provided")

    
    """
        Description:
            Method sends command to pressure device through serial
            port controller
    """
    def sendCommand(self, com):
        if self.commCont is not None:
            self.commCont.writeSerial(com)
            
    def open(self):
        self.commCont.serialOpen()
        
            
    def close(self):
        if self.isOpen():
            self.commCont.serialClose()
        
    def isOpen(self):
        return self.commCont.isOpen()