import sys, os
import time

#sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lsm9ds1_rjg import Driver, I2CTransport, SPITransport


class LSM9DS1:
    """This example shows how to poll the sensor for new data.
    It queries the sensor to discover when the accelerometer/gyro
    has new data and then reads all the sensors."""
    def __init__(self):
        #self.driver = self._create_spi_driver()
        self.driver = self._create_i2c_driver()
        self.driver.configure()

    @staticmethod
    def _create_i2c_driver() -> Driver:
        return Driver(
            I2CTransport(1, I2CTransport.I2C_AG_ADDRESS),
            I2CTransport(1, I2CTransport.I2C_MAG_ADDRESS))

    @staticmethod
    def _create_spi_driver() -> Driver:
        return Driver(
            SPITransport(0, False),
            SPITransport(1, True))

    def main(self):
        try:
            count = 0
            while count < 2000:
                ag_data_ready = self.driver.read_ag_status().accelerometer_data_available
                if ag_data_ready:
                    self.read_ag()
                    count += 1
                    time.sleep(0.05)
        finally:
            self.driver.close()

    def read_gyro(self):
        try:
            ag_data_ready = self.driver.read_ag_status().accelerometer_data_availabe
            if ag_data_ready:
                temp, acc, gyro = self.driver.read_ag_data()
                return gyro
            else:
                return None
        except Exception:
            pass

    def read_acc(self):
        temp, acc, gyro = self.driver.read_ag_data()
        return acc


    def read_ag(self):
        temp, acc, gyro = self.driver.read_ag_data()
        print('Temp:{} Acc:{} Gryo:{}'.format(temp, acc, gyro))

    def read_magnetometer(self):
        mag = self.driver.read_magnetometer()
        print('Mag {}'.format(mag))


if __name__ == '__main__':
    LSM9DS1().main()
