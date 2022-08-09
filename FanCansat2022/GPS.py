import serial
from . import micropyGPS
import threading
import time

class GPS(threading.Thread): 
  def __init__(self): 
      super(myThread, self).__init__()
      self.gps = micropyGPS.MicropyGPS(9, 'dd') # MicroGPSオブジェクトを生成する。
                                     # 引数はタイムゾーンの時差と出力フォーマット

  def run(self):#使うときはrun()じゃなくてstart()
      self.s = serial.Serial('/dev/serial0', 9600, timeout=10)
      self.s.readline() # 最初の1行は中途半端なデーターが読めることがあるので、捨てる
      while True:
          sentence = s.readline().decode('utf-8') # GPSデーターを読み、文字列に変換する
          if sentence[0] != '$': # 先頭が'$'でなければ捨てる
              continue
          for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
              gps.update(x)
               
if __name__ == '__main__':
     Gps = GPS.GPS()
     Gps.start()
     while True:
       x = Gps.latitude[0]
       y = Gps.longitude[0]
       print('緯度経度: %2.8f, %2.8f' % (gps.latitude[0], gps.longitude[0]))
       time.sleep(3.0)
