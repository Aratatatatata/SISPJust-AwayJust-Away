import smbus
import time
import math

class ACC:
		def __init__(self):
				
				self.ADDR_A = 0x6a
				self.ADDR_G = 0x6a
				self.ADDR_M = 0x1c

				self.GET_G_CMD = 0x18
				self.GET_A_CMD = 0x28
				self.GET_M_CMD = 0x28
 
				self.CTRL_REG3_M = 0x22
				self.CTRL_REG4 = 0x1e
				self.CTRL_REG5_XL = 0x1f
				self.CTRL_REG6_XL = 0x20
				self.CTRL_REG1_G = 0x10

				self.CTRL_REG8 = 0x22
				self.CTRL_REG2_M = 0x21

				self.ACCELRANGE_2G = 0b00 << 3
				self.MAGGAIN_4GAUSS = 0b00 << 5
				self.GYROSCALE_245DPS = 0b00 << 3

				self.ACCEL_MG_LSB_2G = 0.061
				self.MAG_MGAUSS_4GAUSS = 0.14
				self.GRAVITY = 9.80665

				self.bus = smbus.SMBus(1)

				self.bus.write_byte_data(self.ADDR_A, self.CTRL_REG8, 0x05)
				self.bus.write_byte_data(self.ADDR_M, self.CTRL_REG2_M, 0x0c)

				time.sleep(0.1)

				self.bus.write_byte_data(self.ADDR_G, self.CTRL_REG1_G, 0xc0) # gyro
				self.bus.write_byte_data(self.ADDR_A, self.CTRL_REG5_XL, 0x38) # acc
				self.bus.write_byte_data(self.ADDR_A, self.CTRL_REG6_XL, 0xc0) # acc
				self.bus.write_byte_data(self.ADDR_M, self.CTRL_REG3_M, 0x00) # mag
				
				reg_a = self.bus.read_byte_data(self.ADDR_A, self.CTRL_REG6_XL)
				reg_a = (reg_a & ~(0b0001100)) & 0xff
				reg_a |= self.ACCELRANGE_2G
				self.bus.write_byte_data(self.ADDR_A, self.CTRL_REG6_XL, reg_a)

				reg_m = self.bus.read_byte_data(self.ADDR_M, self.CTRL_REG2_M)
				reg_m = (reg_m & ~(0b01100000)) & 0xff
				reg_m |= self.MAGGAIN_4GAUSS
				self.bus.write_byte_data(self.ADDR_M, self.CTRL_REG2_M, reg_m)

				reg_g = self.bus.read_byte_data(self.ADDR_G, self.CTRL_REG1_G)
				reg_g = (reg_g & ~(0b00011000)) & 0xff
				reg_g |= self.GYROSCALE_245DPS
				self.bus.write_byte_data(self.ADDR_G, self.CTRL_REG1_G, reg_g)

		def offset(self,n):
			return n * 4.0 / 32768

		def hosuu(self, data1, data2):
			x = data1 | ((data2 & 0x7f) << 8)
			if (data2 & 0x80) == 0x80:
				x = x * -1
			return x

		def hosu2(self, x):
			if ((x >> 15) & 1) == 1:
				x -= 1
				return (~x) & 0xffff 
			return x

		def get_acc_raw(self):
				data = self.bus.read_i2c_block_data(self.ADDR_A, self.GET_A_CMD, 6)  #OUT_X_L_XL ~ OUT_Z_H_L is 48bits
				x = self.hosu2(data[0] | (data[1] << 8))
				y = self.hosu2(data[2] | (data[3] << 8))
				z = self.hosu2(data[4] | (data[5] << 8))
				
				return x,y,z

		def get_acc(self):
				raw = self.get_acc_raw()
				return list(map(lambda x: x * self.ACCEL_MG_LSB_2G / 1000.0 * self.GRAVITY, raw))

		def get_gyr(self):
				data = self.bus.read_i2c_block_data(self.ADDR_G, self.GET_G_CMD, 6) #OUT_X_L_XL ~ OUT_Z_H_L is 48bits
				x = self.hosu2(self.hosuu(data[0],data[1]))
				y = self.offset(self.hosuu(data[2],data[3]))
				z = self.offset(self.hosuu(data[4],data[5]))
				
				return x,y,z



		def get_mag_raw(self):
				data = self.bus.read_i2c_block_data(self.ADDR_M, self.GET_M_CMD, 6) #OUT_X_L_XL ~ OUT_Z_H_L is 48bits
				x = self.hosu2(data[0] | (data[1] << 8))
				y = self.hosu2(data[2] | (data[3] << 8))
				z = self.hosu2(data[4] | (data[5] << 8))
				
				return x,y,z

		def get_mag(self):
				raw = self.get_mag_raw()
				return list(map(lambda x: x * self.MAG_MGAUSS_4GAUSS / 1000.0, raw))

		def get_direction(self):
				x, y, z = self.get_mag()
				theta = math.degrees(math.atan2(y, x))
				return 90 - theta 


		def auto_get_data(self):
				while True:
								print("acc:", self.get_acc())
								print("gyr:", self.get_gyr())
								print("mag:", self.get_mag())
								time.sleep(1)


