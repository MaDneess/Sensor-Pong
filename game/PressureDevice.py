import time

from StaticUtils import StaticUtils
from CommUtils import CommUtils
from CommController import CommController

class PressureDevice:
    DATA_SIZE = 100
    DATA_MIDDLE_POINT = 0
    READING = 0
    commCont = None
    
    def __init__(self, args):
        self.commCont = CommController(args)
        if self.commCont is None:
            raise Exception(CommUtils.CMD_ERROR, CommUtils.ConnectionException)
        
    def calibrate(self):
        # prepare readings list
        readings = []
        while len(readings) <= 100:
            time.sleep(.3)
            readings.append(self.getReadings())
        # find regular mean
        reg_mean = self.mean(readings)
        # sort readings and find median value
        StaticUtils.mergeSort(readings, 0, len(readings)-1)
        median = self.median(readings)
        # format readings from extreme values and find trimmed mean
        readings = self.formatReadings(readings, 20)
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
    def getReadings(self):
        temp = None
        while (temp is None) or (not temp[1]):
            temp = StaticUtils.floatTryParse( self.commCont.readBuffer() )
            if (temp is not None) and (temp[1]):
                return round(temp[0], 2)
    
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