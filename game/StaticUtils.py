"""
StaticUtils.py used to store all static utility methods only

author: Aleksej Zaicev
date: 24/07/2018

"""
from datetime import datetime

class StaticUtils:

    @staticmethod
    def printBanner():
        print("################################################")
        print("################################################")
        print("####              SENSOR-PONG               ####")
        print("####          BHGE, PiCoding club           ####")
        print("################################################")
        print("################################################\n")

        
    @staticmethod
    def printMessage(status, msg):
        print(str(datetime.now()) + " --- " + str(status) + " : " + msg)    

    @staticmethod
    def getSeconds(dt):
        dt = str(dt).split(':')
        dt = dt[2]
        dt = dt.split('.')
        return int(dt[0])
        

    @staticmethod
    def intTryParse(value):
        try:
            return int(value), True
        except ValueError:
            return value, False
        
    @staticmethod
    def floatTryParse(value):
        if value is not None:
            try:
                return float(value), True
            except ValueError:
                return value, False

    @staticmethod
    def encodeData(data):
        return data.encode('utf-8', 'ignore')

    @staticmethod
    def decodeData(data):
        return data.decode('utf-8', 'ignore')

    @staticmethod
    def mergeSort(data, start, end):
        # encapsulated inner function
        def merge(dt, start, mid, end):
            n1 = mid - start + 1
            n2 = end- mid
         
            # create temp arrays
            START = [0] * (n1)
            END = [0] * (n2)
         
            # Copy data to temp arrays L[] and R[]
            for i in range(0 , n1):
                START[i] = dt[start + i]
         
            for j in range(0 , n2):
                END[j] = dt[mid + 1 + j]
         
            # Merge the temp arrays back into arr[l..r]
            i = 0     # Initial index of first subarray
            j = 0     # Initial index of second subarray
            k = start     # Initial index of merged subarray
         
            while i < n1 and j < n2 :
                if START[i] <= END[j]:
                    dt[k] = START[i]
                    i += 1
                else:
                    dt[k] = END[j]
                    j += 1
                k += 1
         
            # Copy the remaining elements of L[], if there
            # are any
            while i < n1:
                dt[k] = START[i]
                i += 1
                k += 1
         
            # Copy the remaining elements of R[], if there
            # are any
            while j < n2:
                dt[k] = END[j]
                j += 1
                k += 1
        # static mergeSort method
        if start < end:
            m = int((start + (end -1))/2)
            StaticUtils.mergeSort(data, start, m)
            StaticUtils.mergeSort(data, m+1, end)
            merge(data, start, m, end)



