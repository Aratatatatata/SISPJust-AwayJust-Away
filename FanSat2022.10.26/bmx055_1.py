from smbus import SMBus
import time
import math

# I2C
class bmx055:
  ACCL_ADDR = 0x19
  ACCL_R_ADDR = 0x02
  GYRO_ADDR = 0x69
  GYRO_R_ADDR = 0x02
  MAG_ADDR = 0x13
  MAG_R_ADDR = 0x42
  i2c = SMBus(1)
  def __init__(self):
    # acc_data_setup : 加速度の値をセットアップ
    self.i2c.write_byte_data(self.ACCL_ADDR, 0x0F, 0x03)
    self.i2c.write_byte_data(self.ACCL_ADDR, 0x10, 0x08)
    self.i2c.write_byte_data(self.ACCL_ADDR, 0x11, 0x00)
    time.sleep(0.5)
    # gyr_data_setup : ジャイロ値をセットアップ
    self.i2c.write_byte_data(GYRO_ADDR, 0x0F, 0x04)
    self.i2c.write_byte_data(GYRO_ADDR, 0x10, 0x07)
    self.i2c.write_byte_data(GYRO_ADDR, 0x11, 0x00)
    time.sleep(0.5)
    # mag_data_setup : 地磁気値をセットアップ
    #data = i2c.read_byte_data(MAG_ADDR, 0x4B)
    if(data == 0):
        self.i2c.write_byte_data(MAG_ADDR, 0x4B, 0x83)
        time.sleep(0.5)
    self.i2c.write_byte_data(MAG_ADDR, 0x4B, 0x01)
    self.i2c.write_byte_data(MAG_ADDR, 0x4C, 0x00)
    self.i2c.write_byte_data(MAG_ADDR, 0x4E, 0x84)
    self.i2c.write_byte_data(MAG_ADDR, 0x51, 0x04)
    self.i2c.write_byte_data(MAG_ADDR, 0x52, 0x16)
    time.sleep(0.5)
  
  def acc_value(self):
    data = [0, 0, 0, 0, 0, 0]
    acc_data = [0.0, 0.0, 0.0]
    try:
        for i in range(6):
            data[i] = self.i2c.read_byte_data(self.ACCL_ADDR, self.ACCL_R_ADDR + i)
        for i in range(3):
            acc_data[i] = ((data[2*i + 1] * 256) + int(data[2*i] & 0xF0)) / 16
            if acc_data[i] > 2047:
                acc_data[i] -= 4096
            acc_data[i] *= 0.0098
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    return acc_data

  def gyro_value(self):
    data = [0, 0, 0, 0, 0, 0]
    gyro_data = [0.0, 0.0, 0.0]
    try:
        for i in range(6):
            data[i] = i2c.read_byte_data(GYRO_ADDR, GYRO_R_ADDR + i)
        for i in range(3):
            gyro_data[i] = (data[2*i + 1] * 256) + data[2*i]
            if gyro_data[i] > 32767:
                gyro_data[i] -= 65536
            gyro_data[i] *= 0.0038
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    return gyro_data
  def mag_value(self):
    data = [0, 0, 0, 0, 0, 0, 0, 0]
    mag_data = [0.0, 0.0, 0.0]
    try:
        for i in range(8):
            data[i] = i2c.read_byte_data(MAG_ADDR, MAG_R_ADDR + i)
        for i in range(3):
            if i != 2:
                mag_data[i] = ((data[2*i + 1] * 256) + (data[2*i] & 0xF8)) / 8
                if mag_data[i] > 4095:
                    mag_data[i] -= 8192
            else:
                mag_data[i] = ((data[2*i + 1] * 256) + (data[2*i] & 0xFE)) / 2
                if mag_data[i] > 16383:
                    mag_data[i] -= 32768
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    return mag_data

if __name__ == "__main__":
    bmx = bmx055()
    time.sleep(0.1)

    while True:
        acc = bmx.acc_value()
        #gyro= bmx.gyro_value()
        #mag = bmx.mag_value()
        print("Accl -> x:{}, y:{}, z: {}".format(acc[0], acc[1], acc[2]))
        #print("Gyro -> x:{}, y:{}, z: {}".format(gyro[0], gyro[1], gyro[2]))
        #print("Mag -> x:{}, y:{}, z: {}".format(mag[0], mag[1], mag[2]))
        print("\n")
        time.sleep(0.1)