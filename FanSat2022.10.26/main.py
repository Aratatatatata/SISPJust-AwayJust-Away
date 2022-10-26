import csv
import datetime
import time
import pytz
import os
import math
import sys
import GPS
import servo
import Controller
import bmx055
def main():
    
#インスタンスの作成
    con = Controller.Controller()
    l_servo = servo.servo(12)
    r_servo = servo.servo(18)
    gps = GPS.GPS()
    bmx = bmx055.bmx055()
    now_time = datetime.datetime.now()
    filename = 'testdata'
    for i in range(10):
        filename_str=filename+'_'+str(i)+'.csv'
        if(os.path.exists(filename_str)==False):
            with open(filename_str, 'a',newline="") as f:
                writer = csv.writer(f)
                writer.writerow(['RUN_START'])
                writer.writerow(['time','latitude','longitude','acc/let'])
            break
    gps.start()
    count = 0
    
#落下検知
    while True:
        acc = bmx.acc_value() #加速度の取得
        #GPSのデータをcsvに出力する.gps.data, gps.timestamp, gps.latitude, gps.longitudeを使用(検証する)
        #accno0,1,2=x,y,z
        with open(filename_str,'a',newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['fall_st',gps.gps.timestamp[0],gps.gps.timestamp[1],gps.gps.timestamp[2],'latitude',gps.gps.latitude[0],'longitude',gps.gps.longitude[0],'acc',acc[0],acc[1],acc[2]])
        if(-15 < acc[0] and acc[0] < 15 and -15 < acc[1] and acc[1] < 15 and -15 < acc[2] and acc[2] < 15):#全部の値が規定値以下になれば開始
            count += 1
        else:
            count = 0
        if(count >= 15):
            break
        time.sleep(0.05)

#制御開始

    gps_x = gps.gps.longitude[0]
    gps_y = gps.gps.latitude[0]
    acc = bmx.acc_value()
    with open(filename_str,'a',newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['fall_end',gps.gps.timestamp[0],gps.gps.timestamp[1],gps.gps.timestamp[2],'latitude',gps.gps.latitude[0],'longitude',gps.gps.longitude[0],'acc',acc[0],acc[1],acc[2]])
    old_x, old_y = gps_x, gps_y
    i = 0

    while True:
        gps_x = gps.gps.longitude[0]
        gps_y = gps.gps.latitude[0]
        
        dir_x, dir_y = con.set_goal(gps_x, gps_y)
        let = con.dis_gps(old_x, old_y, gps_x, gps_y, dir_x, dir_y)
        with open(filename_str,'a',newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['control',gps.gps.timestamp[0],gps.gps.timestamp[1],gps.gps.timestamp[2],'latitude',gps.gps.latitude[0],'longitude',gps.gps.longitude[0],'acc',acc[0],acc[1],acc[2],let])

#サーボモータを動かす
        if let > 0:
            l_servo.write(180)
            r_servo.write(0)
            print("hidari")
        elif let == 0:
            l_servo.write(0)
            r_servo.write(0)
            print("mae")
        else:
            r_servo.write(180)
            l_servo.write(0)
            print("migi")
        print(old_x, old_y, gps_x, gps_y, dir_x, dir_y)
            
        old_x, old_y = gps_x, gps_y
        time.sleep(1.0)
        i += 1
        if(i > 60):
            break
    del l_servo
    del r_servo
    with open(filename_str, 'a',newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['RUN_END'])
    sys.exit()
    
if __name__ == '__main__':
    main()
