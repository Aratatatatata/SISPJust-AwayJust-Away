import os
import time
from typing import Tuple, List

from .abstract_transport import AbstractTransport
from .ag_status import AGStatus
from .magnetometer_status import MagnetometerStatus


class Driver:
    AG_ID = 0b01101000
    MAG_ID = 0b00111101

    def __init__(self, ag_protocol: AbstractTransport, magnetometer_protocol: AbstractTransport, high_priority: bool = False):
        self.ag = ag_protocol
        self.mag = magnetometer_protocol
        # Needs to be a high priority process or it'll drop samples
        # when other processes are under heavy load.
        if high_priority:
            priority = os.sched_get_priority_max(os.SCHED_FIFO)
            param = os.sched_param(priority)
            os.sched_setscheduler(0, os.SCHED_FIFO, param)

    def configure(self):
        """Resets the device and configures it"""
        ###################################################
        #   - Bit 0 - SW_RESET - software reset for accelerometer and gyro - default 0
        #   - Bit 2 - IF_ADD_INC - automatic register increment for multibyte access - default 1
        #   - Bit 6 - BDU - Block data update . Ensures high and low bytes come from
        #             the same sample. Not necessary if waiting for data ready - default 0
        self.ag.write_byte(Register.CTRL_REG8, 0x05)
        # 0x08 - reboot magnetometer, +/- 4 Gauss full scale - fixes occasional magnetometer hang
        # 0x04 - soft reset magnetometer, +/- 4 Gauss full scale
        self.mag.write_byte(Register.CTRL_REG2_M, 0x08)
        time.sleep(0.01)    # Wait for reset
        ###################################################
        # Confirm that we're connected to the device
        if self.ag.read_byte(Register.WHO_AM_I) != Driver.AG_ID:
            raise RuntimeError('Could not find LSM9DS1 Acceleromter/Gyro. Check wiring and port numbers.')
        if self.mag.read_byte(Register.WHO_AM_I_M) != Driver.MAG_ID:
            raise RuntimeError('Could not find LSM9DS1 Magnetometer. Check wiring and port numbers.')
        ###################################################
        # Set up output data rate for Accelerometer and Gyro if using both
        # Use CTRL_REG2_G and CTRL_REG3_G to control the optional additional filters
        # 0x6A - 500 dps, 119 Hz ODR, 38Hz cut off (31 Hz Cut off if HP filter is enabled)
        # 0x8A - 500 dps, 238 Hz ODR, 76Hz cut off (63 Hz Cut off if HP filter is enabled)
        # 0xAA - 500 dps, 476 Hz ODR, 100Hz cut off (57 Hz Cut off if HP filter is enabled)
        # 0x00 - disabled
        self.ag.write_byte(Register.CTRL_REG1_G, 0x8A)
        # 0x03 - Enable LPF2 - Frequency set by REG1 (2nd Low Pass Filter)
        # self.ag.write_byte(Register.CTRL_REG2_G, 0x03)
        # 0x45   - Enable High Pass Filter at (0.2 Hz @ 119 ODR) or (0.5 Hz @ 238 ODR)
        # self.ag.write_byte(Register.CTRL_REG3_G, 0x45)
        ###################################################
        # Set up Accelerometer
        # 0xC0 - Set to +- 2G, 119 Hz ODR, 50 Hz BW (Frequency is ignored if Gryo is enabled)
        # 0x87 - Set to +- 2G, 238 Hz ODR, 50 Hz BW (Frequency is ignored if Gryo is enabled)
        self.ag.write_byte(Register.CTRL_REG6_XL, 0x87)
        # 0x01 INT1_A/G pin set by accelerometer data ready
        self.ag.write_byte(Register.INT1_CTRL, 0x01)
        ###################################################
        # Set up magnetometer
        # MSB enables temperature compensation
        # 0x98 - 40 Hz ODR, Enable Temp Comp
        # 0x9C - 80 Hz ODR, Enable Temp Comp
        # 0x18 - 40 Hz ODR, Disable Temp Comp
        # 0x1C - 80 Hz ODR, Enable Temp Comp
        # 0xE2 - 155 Hz ODR, Enable Temp Comp, x and y ultra high performance
        # 0xC2 - 300 Hz ODR, Enable Temp Comp, x and y high performance
        # 0xA2 - 560 Hz ODR, Enable Temp Comp, x and y medium performance
        # 0x82 - 1000 Hz ODR, Enable Temp Comp, x and y low performance
        self.mag.write_byte(Register.CTRL_REG1_M, 0xC2)
        # 0x00 - Magnetometer continuous operation - I2C enabled
        # 0x80 - Magnetometer continuous operation - I2C disabled
        self.mag.write_byte(Register.CTRL_REG3_M, 0x00)
        # 0x08 - z axi high performance mode - doesn't seem to do anything
        self.mag.write_byte(Register.CTRL_REG4_M, 0x08)
        # Enable BDU (block data update) to ensure high and low bytes come from the same sample
        self.mag.write_byte(Register.CTRL_REG5_M, 0x40)

    def close(self):
        """Closes the I2C/SPI connection. This must be called on shutdown."""
        self.ag.close()
        self.mag.close()

    def ag_data_ready(self, timeout_millis: int) -> bool:
        return self.ag.data_ready(timeout_millis)

    def read_ag_status(self) -> AGStatus:
        """Returns the status byte for the accelerometer and gyroscope."""
        data = self.ag.read_byte(Register.STATUS_REG)
        return AGStatus(data)

    def read_ag_data(self) -> Tuple[int, List[int], List[int]]:
        """Returns the current temperature, acceleration and angular velocity
        values in one go. This is faster than fetching them independently.
        These values can be invalid unless they're read when the data is ready."""
        data = self.ag.read_bytes(Register.OUT_TEMP_L, 14)
        temp = Driver.to_int16(data[0:2])
        gyro = Driver.to_vector_left_to_right_hand_rule(data[2:8])
        acc = Driver.to_vector_left_to_right_hand_rule(data[8:14])
        return temp, acc, gyro

    def read_temperature(self) -> int:
        """Reads the temperature. See also read_ag_data()"""
        data = self.ag.read_bytes(Register.OUT_TEMP_L, 2)
        return Driver.to_int16(data)

    def read_acceleration(self) -> List[int]:
        """Reads the accelerations. See also read_ag_data()"""
        data = self.ag.read_bytes(Register.OUT_X_XL, 6)
        return Driver.to_vector_left_to_right_hand_rule(data)

    def read_gyroscope(self) -> List[int]:
        """Reads the angular velocities. See also read_ag_data()"""
        data = self.ag.read_bytes(Register.OUT_X_G, 6)
        return Driver.to_vector_left_to_right_hand_rule(data)

    def magnetometer_data_ready(self, timout_millis: int) -> bool:
        return self.mag.data_ready(timout_millis)

    def read_magnetometer_status(self) -> MagnetometerStatus:
        """Returns the status byte for the magnetometer"""
        data = self.mag.read_byte(Register.STATUS_REG_M)
        return MagnetometerStatus(data)

    def read_magnetometer(self) -> List[int]:
        """Reads the magnetometer field strengths"""
        data = self.mag.read_bytes(Register.OUT_X_L_M, 6)
        return Driver.to_vector(data)

    @staticmethod
    def to_vector(data: List[int]) -> List[int]:
        return [Driver.to_int16(data[0:2]), Driver.to_int16(data[2:4]), Driver.to_int16(data[4:6])]

    @staticmethod
    def to_vector_left_to_right_hand_rule(data: List[int]) -> List[int]:
        """Like to_vector except it converts from the left to the right hand rule
        by negating the x-axis."""
        return [-Driver.to_int16(data[0:2]), Driver.to_int16(data[2:4]), Driver.to_int16(data[4:6])]

    @staticmethod
    def to_int16(data: List[int]) -> int:
        """
        Converts little endian bytes into a signed 16-bit integer
        :param data: 16bit int in little endian, two's complement form
        :return: an integer
        """
        return int.from_bytes(data, byteorder='little', signed=True)


class Register:
    """Register constants"""
    WHO_AM_I = 0x0F
    CTRL_REG1_G = 0x10
    CTRL_REG2_G = 0x11
    CTRL_REG3_G = 0x12
    OUT_TEMP_L = 0x15
    STATUS_REG = 0x17
    OUT_X_G = 0x18
    CTRL_REG4 = 0x1E
    CTRL_REG5_XL = 0x1F
    CTRL_REG6_XL = 0x20
    CTRL_REG7_XL = 0x21
    CTRL_REG8 = 0x22
    CTRL_REG9 = 0x23
    CTRL_REG10 = 0x24
    OUT_X_XL = 0x28
    REFERENCE_G = 0x0B
    INT1_CTRL = 0x0C
    INT2_CTRL = 0x0D
    WHO_AM_I_M = 0x0F
    CTRL_REG1_M = 0x20
    CTRL_REG2_M = 0x21
    CTRL_REG3_M = 0x22
    CTRL_REG4_M = 0x23
    CTRL_REG5_M = 0x24
    STATUS_REG_M = 0x27
    OUT_X_L_M = 0x28
