import csv
from datetime import datetime
import time
import pytz
import os
import math
import sys

import GPS
import servo
import Controller
import csvWriter
import bmx055
def main():
    
#インスタンスの作成 check

    con = Controller.Controller()
    my_csv = csvWriter.csvWriter()
    gps = GPS.GPS()
    bmx = bmx055.bmx055()
    gps.start()
    count = 0
    
    while True:
       acc = bmx.acc_value() #加速度の取得
       #GPSのデータをcsvに出力する.gps.data, gps.timestamp, gps.latitude, gps.longitudeを使用(検証する)
       my_csv.write([gps.timestamp[0],gps.timestamp[1],gps.timestamp[2],gps.latitude[0],gps.longitude[0],acc_x,acc_y,acc_z,0,0])
       if(-50 < acc[0] and acc[0] < 50    and    -50 < acc[1] and acc[1] < 50    and    -50 < acc[2] and acc[2] < 50):#全部の値が規定値以下になれば開始
            count += 1
              else:
                count = 0

        if(count >= 15):
            break
        time.sleep(0.05)