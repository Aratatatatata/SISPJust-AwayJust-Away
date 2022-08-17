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
    gps_x = gps.gps.longitude[0]
    gps_y = gps.gps.latitude[0]
    old_x, old_y = gps_x, gps_y
    i = 0
    while True:
      gps_x = gps.gps.longitude[0]
      gps_y = gps.gps.latitude[0]
      dir_x, dir_y = con.set_goal(gps_x, gps_y)
      let = con.dis_gps(old_x, old_y, gps_x, gps_y, dir_x, dir_y)
      my_csv.write([gps.gps.timestamp[0],gps.gps.timestamp[1],gps.gps.timestamp[2],gps.gps.latitude[0],gps.gps.longitude[0],let])
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
