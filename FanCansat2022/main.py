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
    
#インスタンスの作成

    con = Controller.Controller()
    my_csv = csvWriter.csvWriter()
    gps = GPS.GPS()
    bmx = bmx055.bmx055()
    gps.start()
    count = 0

#落下検知
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

#制御開始

  gps_x = gps.longitude[0]
  gps_y = gps.latitude[0]

  acc = bmx.acc_value()
  my_csv.write([gps.timestamp[0],gps.timestamp[1],gps.timestamp[2],gps.latitude[0],gps.longitude[0],acc[0],acc[1],acc[2],0,0])
  old_x, old_y = gps_x, gps_y
  i = 0

    
  while True:
        gps_x = gps.longitude[0]
        gps_y = gps.latitude[0]
        
        dir_x, dir_y = con.set_goal(gps_x, gps_y)
        let = con.dis_gps(old_x, old_y, gps_x, gps_y, dir_x, dir_y)
        my_csv.write([gps.timestamp[0],gps.timestamp[1],gps.timestamp[2],gps.latitude[0],gps.longitude[0],let])
         #サーボモータを動かす
	     if let > 0:
             l_servo.write(180)
             r_servo.write(0)
         elif let = 0:
             l_servo.write(0)
             r_servo.write(0)
         else:
             r_servo.write(180)
             l_servo.write(0)

              
       old_x, old_y = gps_x, gps_y
        time.sleep(0.5)
        i += 1
        if(i > 60):
            break

  del l_servo
  del r_servo
  sys.exit()
    

if __name__ == '__main__':
    main()
