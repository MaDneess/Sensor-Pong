"""
    Name: sensor_device.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
import threading
from json import JSONDecodeError

import game_utils
from static_utils import StaticUtils
from comm_serial import CommSerial
import comm_utils
import json


class SensorDevice(threading.Thread):
    """Description: pressure device class defines basic interaction with device"""

    def __init__(self, args, board):
        threading.Thread.__init__(self)
        self.comm_serial = CommSerial(args)
        self.board = board
        self.minimum_point = 80
        self.maximum_point = 497
        self.reading_1 = 0
        self.reading_2 = 0
        self.started = StaticUtils.get_millis()
        self.middle_point = 0
        StaticUtils.print_message(comm_utils.CMD_DEBUG, "Initialized")

    def run(self):
        """Description: threads runnable method"""

        while self.board.state != game_utils.EXIT:
            while self.is_open() and self.board.state == game_utils.IN_GAME:
                readings = self.get()
                self.reading_1, self.reading_2 = readings
        # close serial on exit
        self.close()

    def get(self):
        """Description: methods get single reading from device"""

        try:
            data_dict = json.loads(self.comm_serial.read_buffer())
        except JSONDecodeError:
            StaticUtils.print_message(comm_utils.CMD_DEBUG, "Failed to parse json string")
            return -1, -1
        StaticUtils.print_message(comm_utils.CMD_DEBUG, str(data_dict))
        return data_dict["sensor1"], data_dict["sensor2"]

    def send_command(self, msg):
        """Description: method sends command to pressure device through serial
        port controller
        """

        if self.comm_serial is not None:
            self.comm_serial.write_serial(msg)

    def open(self):
        """Description: method opens serial port"""

        self.comm_serial.serial_open()

    def close(self):
        """Description: method closes serial port"""

        if self.is_open():
            self.comm_serial.serial_close()

    def is_open(self):
        """Description: method checks serial port state"""

        return self.comm_serial.is_open()
