"""
    Name: comm_utils.py
    Author: Aleksej Z
    Date: 2018/08/18
"""

CMD_OK = 200
CMD_ERROR = 500
CMD_RESPONSE = 201

CALIBRATION_DATA_SIZE = 100

CONNECTION_EXCEPTION = "No opened serial port detected"
OPENED_CONNECTION_EXCEPTION = "Serial port is already opened"
INVALID_PORT_EXCEPTION = "Serial port provided is invalid"
DEVICE_NOT_FOUND_EXCEPTION = "No device connected to port: "
IDENTICAL_PORTS_EXCEPTION = "Identical ports found. Devices should have unique ports"

SERIAL_PORT_START_UNIX = "/dev/tty"
SERIAL_PORT_START_WIN = "COM"
