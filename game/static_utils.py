"""
    Name: static_utils.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
import time
from datetime import datetime


class StaticUtils:
    """Description: utility class contains global function"""

    @staticmethod
    def print_banner():
        """Description: methods prints welcome banner on start"""

        print("################################################")
        print("################################################")
        print("####              SENSOR-PONG               ####")
        print("####          BHGE, PiCoding club           ####")
        print("################################################")
        print("################################################\n")

    @staticmethod
    def get_millis():
        """Description: method return current time millis
        :return: Milliseconds
        """

        return int(round(time.time() * 1000))

    @staticmethod
    def print_message(status, msg):
        """Description: method print message with status code into the logger"""

        print(str(datetime.now()) + " --- " + str(status) + " : " + msg)

    @staticmethod
    def int_try_parse(value):
        """Description: method converts value into valid integer
        :param: Value to convert
        :return: Integer value and boolean state
        """

        try:
            return int(value), True
        except ValueError:
            return value, False

    @staticmethod
    def float_try_parse(value):
        """Description: method converts value into valid float
        :param: Value to convert
        :return: Float value and boolean state
        """

        try:
            return float(value), True
        except ValueError:
            return value, False

    @staticmethod
    def mean(values):
        """Description: method find list mean (regular average value)
        :param: Value list
        :return: Mean of provided values
        """

        return sum(values) / len(values)

    @staticmethod
    def median(values):
        """Description: method finds median value of a given array
        :param {values}
        """

        if len(values) % 2 == 0:
            mid = int((len(values)-1) / 2)
            num = (values[mid] + values[mid+1]) / 2
        else:
            num = values[int(len(values) / 2)]
        return num

    @staticmethod
    def format_readings(values, ran):
        """Description: method cuts values from a list in a specified range"""

        start = int(len(values)/2) - int(ran/2)
        end = int(len(values)/2) + int(ran/2)
        temp = []
        for i in range(start, end):
            temp.append(values[i])
        return temp

    @staticmethod
    def encode_data(data):
        """Description: method encodes string into utf-8 character string
        :param: Data to encode
        :return: utf-8 data
        """

        return data.encode('utf-8', 'ignore')

    @staticmethod
    def decode_data(data):
        """Description: method decodes utf-8 data
        :param: Data to decode
        :return: Decoded data
        """

        return data.decode('utf-8', 'ignore')

    @staticmethod
    def merge_sort(data, start, end):
        """Description: method sorts provided data
        :param: Data to sort
        :param: From where to start
        :param: Until where finish
        """

        def merge(data_sort, data_start, data_mid, data_end):
            """Description: function used by upper merge sort
            :param: Data to sort
            :param: Start of the data
            :param: Middle of data
            :param: End of the data
            """

            num_1 = data_mid - data_start + 1
            num_2 = data_end - data_mid
            # create temp arrays
            temp_1 = [0] * num_1
            temp_2 = [0] * num_2
            # Copy data to temp arrays L[] and R[]
            for i in range(0, num_1):
                temp_1[i] = data_sort[data_start + i]
            for j in range(0, num_2):
                temp_2[j] = data_sort[data_mid + 1 + j]
            # Merge the temp arrays back into arr[l..r]
            i = 0     # Initial index of first sub array
            j = 0     # Initial index of second sub array
            k = data_start     # Initial index of merged sub array
            while i < num_1 and j < num_2:
                if temp_1[i] <= temp_2[j]:
                    data_sort[k] = temp_1[i]
                    i += 1
                else:
                    data_sort[k] = temp_2[j]
                    j += 1
                k += 1
            # Copy the remaining elements of L[], if there
            # are any
            while i < num_1:
                data_sort[k] = temp_1[i]
                i += 1
                k += 1
            # Copy the remaining elements of R[], if there
            # are any
            while j < num_2:
                data_sort[k] = temp_2[j]
                j += 1
                k += 1
        # static merge_sort method
        if start < end:
            mid = int((start + (end - 1))/2)
            StaticUtils.merge_sort(data, start, mid)
            StaticUtils.merge_sort(data, mid + 1, end)
            merge(data, start, mid, end)
