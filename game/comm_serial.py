"""
    Name: comm_serial.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
from serial import Serial
from static_utils import StaticUtils
import comm_utils


class CommSerial:
    """Description: serial communication class providing basic serial functionality"""

    def __init__(self, args):
        if len(args) == 3:
            self.serial = Serial(args[0], int(args[1]), timeout=int(args[2]))
            self.port = args[0]
        elif len(args) == 2:
            self.serial = Serial(args[0], int(args[1]))
            self.port = args[0]
        else:
            StaticUtils.print_message(comm_utils.CMD_ERROR, comm_utils.INVALID_PORT_EXCEPTION)
            raise ValueError(comm_utils.INVALID_PORT_EXCEPTION)
        self.serial_close()

    def read_buffer(self):
        """Description: method reads incoming messages on the opened serial port
        :return: Decoded message read from the buffer
        """

        msg = ""
        if self.serial.inWaiting():
            msg = self.serial.readline()
            print(msg, len(msg), sep="---")
            msg = msg.decode('utf-8', 'ignore')
        return msg

    def write_serial(self, str_msg):
        """Description: method send the message over opened serial port
        :param: Message to send
        """

        msg = str_msg.encode('utf-8', 'ignore')
        self.serial.write(msg)

    def serial_open(self):
        """Description: method opens serial port"""

        if not self.serial.is_open:
            self.serial.open()
            StaticUtils.print_message(comm_utils.CMD_OK,
                                      "Serial port " + self.port + " have been opened.")
        else:
            StaticUtils.print_message(comm_utils.CMD_ERROR, comm_utils.OPENED_CONNECTION_EXCEPTION)

    def serial_close(self):
        """Description: method closes serial port"""

        self.serial.close()
        StaticUtils.print_message(comm_utils.CMD_OK,
                                  "Serial port " + self.port + " have been closed.")

    def is_open(self):
        """Description: method returns serial port state
        :return: Port state
        """

        return self.serial.is_open
