# RPI Serial: /dev/ttyACM0:9600:3
# Windows Serial: COM3:9600:3
from Board import Board
from StaticUtils import StaticUtils
from CommUtils import CommUtils

class Main:
    
    def __init__(self):
        StaticUtils.printBanner()
        #get serial ports details
        port1 = self.getPortDetails(1)
        #port2 = self.getPortDetails(2)
        #while port1 == port2:
        #    StaticUtils.printMessage(CommUtils.CMD_ERROR, CommUtils.IdenticalPortsException)
        #    port1 = self.getPortDetails(1)
        #    port2 = self.getPortDetails(2)
        
        self.board = Board(port1.split(':'), port2=[])
        self.board.run()

    def getPortDetails(self, n):
        temp = input("Device %d, Specify device port, baudrate (opt. timeout)\n{PORT}:{BAUDRATE}:{TIMEOUT}\n" % (n))
        # ask for a valid command until received
        while not self.isValidInput(temp):
            StaticUtils.printMessage(CommUtils.CMD_ERROR, CommUtils.InvalidPortException)
            temp = input("Specify device port, baudrate (opt. timeout)\n{PORT}:{BAUDRATE}:{TIMEOUT}\n")
        return temp
    
    """
        Description:
            Method checks if the specified port is a valid UNIX/WIN serial port
    """
    def isValidSerial(self, port):
        return (CommUtils.SERIAL_PORT_START_UNIX in port) or (CommUtils.SERIAL_PORT_START_WIN in port)
    
    """
        Description:
            Method checks if the provided input was valid
    """
    def isValidInput(self, message):
        if not ((not message) or (message == "")):
            message = message.split(':')
            if (len(message) > 1) and (len(message) < 4) and (self.isValidSerial(message[0])):
                if (StaticUtils.intTryParse(message[1])[1]) and (StaticUtils.intTryParse(message[2])[1]):
                    return True
        return False


if __name__ == "__main__":
    main = Main()
