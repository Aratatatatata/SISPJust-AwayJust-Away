import smbus
import time
import math

ADDR_XG = 0x6a
ADDR_M = 0x1c

GET_G_CMD = 0x18
GET_A_CMD = 0x28
GET_M_CMD = 0x28
 
CTRL_REG3_M = 0x22
CTRL_REG4 = 0x1e
CTRL_REG5_XL = 0x1f
CTRL_REG6_XL = 0x20
CTRL_REG1_G = 0x10

CTRL_REG8 = 0x22
CTRL_REG2_M = 0x21

ACCELRANGE_2G = 0b00 << 3
MAGGAIN_4GAUSS = 0b00 << 5
GYROSCALE_245DPS = 0b00 << 3

ACCEL_MG_LSB_2G = 0.061
MAG_MGAUSS_4GAUSS = 0.14
GYRO_DPS_DIGIT_245DPS = 0.00875
GRAVITY = 9.80665

class LSM9DS1:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        
        self.bus.write_byte_data(ADDR_XG, CTRL_REG8, 0x05)
        self.bus.write_byte_data(ADDR_M, CTRL_REG2_M, 0x0c)

        time.sleep(0.1)

        self.bus.write_byte_data(ADDR_XG, CTRL_REG1_G, 0xc0) # gyro
        self.bus.write_byte_data(ADDR_XG, CTRL_REG5_XL, 0x38) # acc
        self.bus.write_byte_data(ADDR_XG, CTRL_REG6_XL, 0xc0) # acc
        self.bus.write_byte_data(ADDR_M, CTRL_REG3_M, 0x00) # mag

        reg_a = ((self.bus.read_byte_data(ADDR_XG, CTRL_REG6_XL) & ~(0b0001100)) & 0xff) | ACCELRANGE_2G
        self.bus.write_byte_data(ADDR_XG, CTRL_REG6_XL, reg_a)

        reg_m = ((self.bus.read_byte_data(ADDR_M, CTRL_REG2_M) & ~(0b01100000)) & 0xff) | MAGGAIN_4GAUSS
        self.bus.write_byte_data(ADDR_M, CTRL_REG2_M, reg_m)

        reg_g = ((self.bus.read_byte_data(ADDR_XG, CTRL_REG1_G) & ~(0b00011000)) & 0xff) | GYROSCALE_245DPS
        self.bus.write_byte_data(ADDR_XG, CTRL_REG1_G, reg_g)

    def hosu(self, x):
        if ((x >> 15) & 1) == 1:
            x -= 1
            return (~x) & 0xffff 
        return x

    def get_raw(self, address, command):
        data = self.bus.read_i2c_block_data(address, command, 6)  #OUT_X_L_XL ~ OUT_Z_H_L is 48bits
        x = self.hosu(data[0] | (data[1] << 8))
        y = self.hosu(data[2] | (data[3] << 8))
        z = self.hosu(data[4] | (data[5] << 8))

        return x,y,z

    def get_accel(self):
        raw = self.get_raw(ADDR_XG, GET_A_CMD)
        return list(map(lambda x: x * ACCEL_MG_LSB_2G / 1000.0 * GRAVITY, raw))

    def get_gyro(self):
        raw = self.get_raw(ADDR_XG, 0x08 | GET_G_CMD)
        return list(map(lambda x: math.degrees(math.radians(x * GYRO_DPS_DIGIT_245DPS)), raw))
               
    def get_mag(self):
        raw = self.get_mag_raw(ADDR_M, GET_M_CMD)
        return list(map(lambda x: x * MAG_MGAUSS_4GAUSS / 1000.0, raw))

    def get_direction(self):
        x, y, z = self.get_mag() 

    def auto_get_data(self):
        while True:
            print("acc:", self.get_accel())
            print("gyr:", self.get_gyro())
            print("mag:", self.get_mag())
            time.sleep(1)
