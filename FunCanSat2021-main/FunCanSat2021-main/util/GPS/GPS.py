import serial
import time
import threading

from . import micropyGPS

class GPS(threading.Thread):
    lock = threading.Lock()

    def __init__(self, local_offset=0, location_formatting='ddm'):
        super(GPS, self).__init__(daemon = True)
        self.port = serial.Serial('/dev/serial0', 9600, timeout=0)
        self.mpy_gps = micropyGPS.MicropyGPS(local_offset, location_formatting)
    
    def run(self):
        while True:
            time.sleep(0.1)
            try:
                sentence = self.port.readline().decode('utf-8')
                if sentence.startswith('$GPRMC'):
                    for x in sentence:
                        self.mpy_gps.update(x)
            except Exception:
                pass
    
    def thread_acquire(self):
        GPS.lock.acquire()
    
    def thread_release(self):
        GPS.lock.release()

    def get_data(self):
        t = []
        key = ['date', 'timestamp', 'latitude', 'longitude']
        t.append(self.mpy_gps.date)
        t.append(self.mpy_gps.timestamp)
        t.append(self.mpy_gps.latitude)
        t.append(self.mpy_gps.longitude)
        self.d = dict(zip(key, t))
        return self.d
