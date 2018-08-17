"""
    CommUtils.py store variables associated with serial communication
    
    author: Aleksej Zaicev
    date: 24/07/2018
"""
####################################################
class CommUtils:
    """

        Variables:
            CMD_OK, used to identify if message command worked correctly
            CMD_ERROR, identifies if error occurred executing command
            CMD_RESPONSE, identifies serial response
            
    """
    CMD_OK = 200
    CMD_ERROR = 500
    CMD_RESPONSE = 201

    """
        Description:
            Device specific configuration
    """
    CALIBRATION_DATA_SIZE = 100

    """

        Exceptions:
            :param          {ConnectionException}        thrown if no opened serial port detected
            :param          {OpenedConnectionException}  thrown if serial port is already opened
            :param          {InvalidPortException}       thrown, if provided serial port is invalid
            :param          {DeviceNotFoundException}    thrown if no device was detected on the opened port
            
    """
    ConnectionException = "No opened serial port detected"
    OpenedConnectionException = "Serial port is already opened"
    InvalidPortException = "Serial port provided is invalid"
    DeviceNotFoundException = "No device connected to port: "
    IdenticalPortsException = "Identical ports found. Devices should have unique ports"

    """

        Constant variable:
            Used to identify correct path to serial port

    """
    SERIAL_PORT_START_UNIX = "/dev/tty"
    SERIAL_PORT_START_WIN = "COM"
