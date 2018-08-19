"""
    Name: main.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
# RPI Serial: /dev/ttyACM0:9600:3
# Windows Serial: COM3:9600:3
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
                if (len(message) > 1) and (len(message) < 4) and (is_valid_serial(message[0])):
                    if (StaticUtils.int_try_parse(message[1])[1]) and \
                            (StaticUtils.int_try_parse(message[2])[1]):
                        return True
            return False

        temp = input("Device %d, Specify device port, "
                     "baudrate (opt. timeout)\n{PORT}:{BAUDRATE}:{TIMEOUT}\n" % device_num)
        # ask for a valid command until received
        while not is_valid_input(temp):
            StaticUtils.print_message(comm_utils.CMD_ERROR, comm_utils.INVALID_PORT_EXCEPTION)
            temp = input("Specify device port, baudrate "
                         "(opt. timeout)\n{PORT}:{BAUDRATE}:{TIMEOUT}\n")
        return temp

    StaticUtils.print_banner()
    # get serial ports details
    port1 = get_port_details(1)
    # port2 = self.get_port_details(2)
    # while port1 == port2:
    #    StaticUtils.print_message(comm_utils.CMD_ERROR, comm_utils.IDENTICAL_PORTS_EXCEPTION)
    #    port1 = self.get_port_details(1)
    #    port2 = self.get_port_details(2)
    board = Board(port1.split(':'), port2=[])
    board.run()


if __name__ == "__main__":
    start_game()
