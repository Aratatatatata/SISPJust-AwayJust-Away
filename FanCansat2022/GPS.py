from micropyGPS import MicropyGPS
import serial
my_gps = MicropyGPS()
my_sentence = serial.Serial().readline.decode('UTF-8')
for x in my_sentence:
     my_gps.update(x)
