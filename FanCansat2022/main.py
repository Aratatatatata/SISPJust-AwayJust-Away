import csv
from datetime import datetime
import time
import pytz
import os
import math
import sys

from . import GPS
from . import sarvo
from . import Controller
from . import 

def main():
    
    con = Controller.Controller()
    my_csv = MakeCSV()
    
    time.sleep(0.2)
    lsm = simple.LSM9DS1()
    gps = GPS.GPS(9,'dd')
    gps.start()
    count = 0
    while True:
        gps.thread_acquire()
        data = gps.get_data()
        gps.thread_release()
        acc_x, acc_y, acc_z = lsm.read_acc()
        my_csv.write([data['date'][0],data['date'][1],data['date'][2],data['timestamp'][0],data['timestamp'][1],data['timestamp'][2],data['latitude'][0],data['latitude'][1],data['longitude'][0],data['longitude'][1],acc_x,acc_y,acc_z,0,0])
        if(-5000 < acc_z and acc_z < 5000):
            count += 1
        else:
            count = 0

        if(count >= 15):
            break
        time.sleep(0.05)

    gps.thread_acquire()
    data = gps.get_data()
    gps.thread_release()

    gps_x = float(data['longitude'][0])
    gps_y = float(data['latitude'][0])

    acc_x, acc_y, acc_z = lsm.read_acc()
    my_csv.write([data['date'][0],data['date'][1],data['date'][2],data['timestamp'][0],data['timestamp'][1],data['timestamp'][2],data['latitude'][0],data['latitude'][1],data['longitude'][0],data['longitude'][1],acc_x,acc_y,acc_z,0,0])

    con.uturn(gps_x, gps_y, 0, 0)
    time.sleep(1.5)

    old_x, old_y = gps_x, gps_y

    gps.thread_acquire()
    data = gps.get_data()
    gps.thread_release()

    #print('while')
    i = 0
    while True:
        gps.thread_acquire()
        data = gps.get_data()
        gps.thread_release()

        gps_x = float(data['longitude'][0])
        gps_y = float(data['latitude'][0])
        
        dir_x, dir_y = con.direction(gps_x, gps_y)
        LR, let = con.dis_gps(old_x, old_y, gps_x, gps_y, dir_x, dir_y)
        my_csv.write([data['date'][0],
            data['date'][1],data['date'][2],data['timestamp'][0],data['timestamp'][1],
            data['timestamp'][2],data['latitude'][0],data['latitude'][1],data['longitude'][0],data['longitude'][1],
            acc_x,acc_y,acc_z,LR,let])
        old_x, old_y = gps_x, gps_y
        time.sleep(0.5)
        i += 1
        if(i > 60):
            break

    while True:
        pass

    sys.exit()


if __name__ == '__main__':
    main()
