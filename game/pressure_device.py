"""
    Name: pressure_device.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
import time
import threading
import comm_utils
import game_utils
from static_utils import StaticUtils
from comm_serial import CommSerial


class PressureDevice(threading.Thread):
    """Description: pressure device class defines basic interaction with device"""

    def __init__(self, args, board):
        threading.Thread.__init__(self)
        self.comm_serial = CommSerial(args)
        self.board = board
        self.minimum_point = 0
        self.maximum_point = 1
        self.reading = 0
        self.started = StaticUtils.get_millis()
        self.middle_point = 0

    def run(self):
        """Description: threads runnable method"""

        while self.board.state != game_utils.EXIT:
            while self.is_open() and self.board.state == game_utils.IN_GAME:
                if (StaticUtils.get_millis() - self.started) > 350:
                    self.reading = self.get_readings(None, 1)
                    self.started = StaticUtils.get_millis()
        # close serial on exit
        self.close()

    def calibrate_min(self):
        """Description: method takes 5 readings and sets minimum point"""

        self.minimum_point = StaticUtils.mean(self.get_readings([], 5))

    def calibrate_max(self):
        """Description: method takes 5 readings and sets maximum point"""

        self.maximum_point = StaticUtils.mean(self.get_readings([], 5))

    def calibrate(self):
        """Description: method takes 100 reading from the device and calculates middle point"""

        # prepare readings list
        readings = self.get_readings([], comm_utils.CALIBRATION_DATA_SIZE)
        # find regular mean
        reg_mean = StaticUtils.mean(readings)
        # sort readings and find median value
        StaticUtils.merge_sort(readings, 0, len(readings) - 1)
        median = StaticUtils.median(readings)
        # format readings from extreme values and find trimmed mean
        readings = StaticUtils.format_readings(readings, int(comm_utils.CALIBRATION_DATA_SIZE * .2))
        trim_mean = StaticUtils.mean(readings)
        self.middle_point = (reg_mean + median + trim_mean) / 3
        self.reading = self.middle_point

    def get_readings(self, readings, num):
        """Description: method gets string message from the comm controller
        and try parses it into float
        :param: List of readings
        :param: Number of readings
        :returns: List of appended readings or single reading
        :raise: ValueError if number provided is invalid
        """

        def get():
            """Description: methods get single reading from device"""

            temp = StaticUtils.float_try_parse(self.comm_serial.read_buffer())
            while (temp is None) or (not temp[1]):
                temp = StaticUtils.float_try_parse(self.comm_serial.read_buffer())
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
