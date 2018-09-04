"""
    Name: comm_serial.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
from serial import Serial
from serial import SerialException
from game.static_utils import StaticUtils
from game.comm_utils import *


class CommSerial:
    """Description: serial communication class providing basic serial functionality"""

    def __init__(self, args):
        def assign_port(port, baudrate, time=3):
            """Description: method creates serial port object"""

            try:
                serial_port = Serial(port, baudrate, timeout=time)
                return serial_port
            except SerialException as e:
                StaticUtils.print_message(CMD_ERROR, str(e))
                return None

        if len(args) == 3:
            self.serial = assign_port(args[0], int(args[1]), int(args[2]))
        elif len(args) == 2:
            self.serial = assign_port(args[0], int(args[1]))

        if self.serial is not None:
            self.port = args[0]
            self.serial_close()
        else:
            raise SerialException(CONNECTION_EXCEPTION)

    def read_buffer(self):
        """Description: method reads incoming messages on the opened serial port
        :return: Decoded message read from the buffer
        """

        msg = ""
        try:
            if self.serial.inWaiting():
                msg = self.serial.readline()
                msg = msg.decode('utf-8', 'ignore')
                msg = msg[:6]
                print("Parsed message: " + msg)
        except SerialException as ex:
            StaticUtils.print_message(CMD_ERROR, "Failed to read buffer: " + str(ex))
        return msg

    def write_serial(self, str_msg):
        """Description: method send the message over opened serial port
        :param: Message to send
        """

        msg = str_msg.encode('utf-8', 'ignore')
        try:
            self.serial.write(msg)
        except SerialException:
            StaticUtils.print_message(CMD_ERROR, comm_utils.CONNECTION_EXCEPTION)
        except TypeError as ex:
            StaticUtils.print_message(CMD_ERROR, "Failed to send bytes: " + str(ex))

    def serial_open(self):
        """Description: method opens serial port"""

        if not self.serial.is_open:
            self.serial.open()
            StaticUtils.print_message(CMD_OK,
                                      "Serial port " + self.port + " have been opened.")
        else:
            StaticUtils.print_message(CMD_ERROR, comm_utils.OPENED_CONNECTION_EXCEPTION)

    def serial_close(self):
        """Description: method closes serial port"""

        self.serial.close()
        StaticUtils.print_message(CMD_OK,
                                  "Serial port " + self.port + " have been closed.")

    def is_open(self):
        """Description: method returns serial port state
        :return: Port state
        """

        return self.serial.is_open
