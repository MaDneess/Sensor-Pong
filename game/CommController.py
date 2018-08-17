"""
    CommController.py main serial communication controller

    author: Aleksej Zaicev
    date: 24/07/2018
"""

from serial import *
from StaticUtils import StaticUtils
from CommUtils import CommUtils


class CommController:

    def __init__(self, args):
        super().__init__()
        
        if len(args) == 3:
            self.serial = Serial(args[0], int(args[1]), timeout=int(args[2]))
            self.port = args[0]
        elif len(args):
            self.serial = Serial(args[0], int(args[1]))
            self.port = args[0]
        else:
            StaticUtils.printMessage(CommUtils.CMD_ERROR, CommUtils.InvalidPortException)
            raise ValueError(CommUtils.InvalidPortException)
        self.serialClose()
     
    """
        Description:
            Method reads incoming messages on the opened serial port,
            decode them from utf-8
        
        Return:
            :param {str(msg)}
    """
    def readBuffer(self):
        if self.serial.inWaiting():
            msg = self.serial.readline()
            print(msg)
            return msg.decode('utf-8', 'ignore')
    
    """
        Desciption:
            Method encodes string message into utf-8 and send the message
            over opened serial port
        
        :param {str_msg}
    """
    def writeSerial(self, str_msg):
        msg = str_msg.encode('utf-8', 'ignore')
        self.serial.write(msg)
    
    def serialOpen(self):
        if not self.serial.is_open:
            self.serial.open()
            StaticUtils.printMessage(CommUtils.CMD_OK, "Serial port "+self.port+" have been opened.")
            time.sleep(.2)
        else:
            StaticUtils.printMessage(CommUtils.CMD_ERROR, CommUtils.OpenedConnectionException)
    
    """
        Description:
            Closes opened serial port
    """
    def serialClose(self):
        self.serial.close()
        StaticUtils.printMessage(CommUtils.CMD_OK, "Serial port "+self.port+" have been closed.")
        
    def isOpen(self):
        return self.serial.is_open
        