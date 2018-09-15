"""
    Name: main.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
# RPI Serial: /dev/ttyACM0:9600:3
# Windows Serial: COM3:9600:3
from serial import SerialException
from serial import Serial
import comm_utils
from board import Board
from static_utils import StaticUtils


def start_game():
    """Description: method starts game"""

    def get_port_details(device_num):
        """Description: method gets serial port details"""

        def is_valid_input(message):
            """Description: method checks if provided input is valid"""

            def is_valid_serial(port):
                """Description: method checks if provided serial name is valid"""
                return (comm_utils.SERIAL_PORT_START_UNIX in port) or \
                       (comm_utils.SERIAL_PORT_START_WIN in port)

            if not ((not message) or (message == "")):
                message = message.split(':')
                if is_valid_serial(message[0]):
                    if len(message) == 3:
                        if (StaticUtils.int_try_parse(message[1])[1]) and\
                                (StaticUtils.int_try_parse(message[2])[1]):
                            return True
                    elif len(message) == 2:
                        if (StaticUtils.int_try_parse(message[1]))[1]:
                            return True
            return False

        temp = None
        temp = input("Device %d, Specify device port, baudrate (opt. timeout)"
                     "\n{PORT}:{BAUDRATE}:{TIMEOUT}\n" % device_num)
        # ask for a valid command until received
        while not is_valid_input(temp):
            StaticUtils.print_message(comm_utils.CMD_ERROR, comm_utils.INVALID_PORT_EXCEPTION)
            temp = input("Device %d, Specify device port, baudrate (opt. timeout)"
                         "\n{PORT}:{BAUDRATE}:{TIMEOUT}\n" % device_num)
        return temp

    def check_equal_ports(port_1, port_2):
        """Description: function checks if port names are identical
        :param port_1: Port 1 name
        :param port_2: Port 2 name
        """
        while port_1[0] == port_2[0]:
            StaticUtils.print_message(comm_utils.CMD_ERROR, comm_utils.IDENTICAL_PORTS_EXCEPTION)
            port_1 = get_port_details(1)
            port_2 = get_port_details(2)
            port_1 = port_1.split(':')
            port_2 = port_2.split(':')

    StaticUtils.print_banner()
    # get serial ports details
    port1_check, port2_check = False, False
    port1, port2 = None, None
    while not port1_check or not port2_check:
        port1 = get_port_details(1)
        port2 = get_port_details(2)
        port1 = port1.split(':')
        port2 = port2.split(':')
        check_equal_ports(port1, port2)
        try:
            test_comm_serial = Serial(port1[0], int(port1[1]))
            test_comm_serial.close()
            port1_check = True
        except SerialException as e:
            StaticUtils.print_message(comm_utils.CMD_ERROR, str(e))
        try:
            test_comm_serial = Serial(port2[0], int(port2[1]))
            test_comm_serial.close()
            port2_check = True
        except SerialException as e:
            StaticUtils.print_message(str(e))
    board = Board(port1, port2)
    board.run()


if __name__ == "__main__":
    start_game()
