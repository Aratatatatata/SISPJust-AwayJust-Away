import serial
import micropyGPS
import threading
import time

class GPS(threading.Thread): 
  def __init__(self): 
      super(GPS, self).__init__()
      self.gps = micropyGPS.MicropyGPS(9, 'dd') # MicroGPSオブジェクトを生成する。
                                     # 引数はタイムゾーンの時差と出力フォーマット

  def run(self):#使うときはrun()じゃなくてstart()
      s = serial.Serial('/dev/serial0', 9600, timeout=10)
      s.readline() # 最初の1行は中途半端なデーターが読めることがあるので、捨てる
      while True:
          sentence = s.readline().decode('utf-8') # GPSデーターを読み、文字列に変換する
          #if len(sentence) > 0:
          if sentence[0] != '$': # 先頭が'$'でなければ捨てる
              continue
          for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
              self.gps.update(x)
    
if __name__ == '__main__':
     Gps = GPS()
     Gps.start()
     while True:
         if Gps.gps.clean_sentences > 20:
             h = Gps.gps.timestamp[0] if Gps.gps.timestamp[0] < 24 else Gps.gps.timestamp[0] - 24
             print('%2d:%02d:%04.1f' % (h, Gps.gps.timestamp[1], Gps.gps.timestamp[2]))
             x = Gps.gps.latitude[0]
             y = Gps.gps.longitude[0]
             print('緯度経度: %2.8f, %2.8f' % (x, y))
             time.sleep(3.0)