"""
Adafruit IMU interface.

Script to interface with the Adafruit BNO055 IMU sensor.

Created by Eduardo Ponz, Steffan Svendsen, Vincent Joly,
David Michalik, Ivelin Penchev & Simone Jensen.
4th semester, Bachelor in Robotics, AAU. 13-feb-2018.
"""

import logging
import sys
import time

from Adafruit_BNO055 import BNO055


class ImuReader():
    """."""

    def __init__(self):
        """."""
        # Rasp-Pi configuration with serial UART and RST connected to GPIO 18:
        self.bno = BNO055.BNO055(serial_port='/dev/ttyS0', rst=18)

        # Initialize the BNO055 and stop if something went wrong.
        if not self.bno.begin():
            raise RuntimeError('Failed to initialize BNO055! Is the sensor' +
                               'connected?')

        self.check_status()
        self.diagnostics()

    def check_status(self):
        """."""
        # Print system status and self test result.
        status, self_test, error = self.bno.get_system_status()
        print('System status: {0}'.format(status))
        print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
        # Print out an error if system status is in error mode.
        if status == 0x01:
            print('System error: {0}'.format(error))
            print('See datasheet section 4.3.59 for the meaning.')

    def diagnostics(self):
        """."""
        # Print BNO055 software revision and other diagnostic data.
        sw, bl, accel, mag, gyro = self.bno.get_revision()
        print('Software version:   {0}'.format(sw))
        print('Bootloader version: {0}'.format(bl))
        print('Accelerometer ID:   0x{0:02X}'.format(accel))
        print('Magnetometer ID:    0x{0:02X}'.format(mag))
        print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

    def get_calibration_status(self):
        """."""
        sys, gyro, accel, mag = self.bno.get_calibration_status()
        if sys is 3:
            if gyro is 3:
                if accel is 3:
                    if mag is 3:
                        return True
                    else:
                        print("Magnotemeter is not calibrated")
                        return False
                else:
                    print("Accelerometer is not calibrated")
                    return False
            else:
                print("Gyroscope is not calibrated")
                return False
        else:
            print("System is not calibrated")
            return False

    def get_gravity(self):
        """."""
        if self.get_calibration_status():
            x, y, z = self.bno.read_gravity()
            gravity = {}
            gravity['x'] = x
            gravity['y'] = y
            gravity['z'] = z
            return gravity
        else:
            return None

    def get_euler(self):
        """."""
        if self.get_calibration_status():
            heading, roll, pitch = self.bno.read_euler()
            euler = {}
            euler['heading'] = heading
            euler['roll'] = roll
            euler['pitch'] = pitch
            return euler
        else:
            return None

    # Other values you can optionally read:
    # Orientation as a quaternion:
    # x,y,z,w = bno.read_quaterion()
    # Sensor temperature in degrees Celsius:
    # temp_c = bno.read_temp()
    # Magnetometer data (in micro-Teslas):
    # x,y,z = bno.read_magnetometer()
    # Gyroscope data (in degrees per second):
    # x,y,z = bno.read_gyroscope()
    # Accelerometer data (in meters per second squared):
    # x,y,z = bno.read_accelerometer()
    # Linear acceleration data (acceleration from movement, not gravity--
    # returned in meters per second squared):
    # x,y,z = bno.read_linear_acceleration()
    # Gravity acceleration data (acceleration just from gravity--returned
    # in meters per second squared):
    # x,y,z = bno.read_gravity()
    # Sleep for a second until the next reading.


if __name__ == '__main__':
    # Enable verbose debug logging if -v is passed as a parameter.
    if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
        logging.basicConfig(level=logging.DEBUG)

    imu = ImuReader()
    print('Reading BNO055 data, press Ctrl-C to quit...')

    while True:
        gravity = imu.get_gravity()
        euler = imu.get_euler()
        print('Heading={0:0.2F} '.format(euler['heading']) +
              'Roll={0:0.2F} '.format(euler['roll']) +
              'Pitch={0:0.2F}'.format(euler['pitch']) +
              '\tX={} '.format(gravity['x']) +
              'Y={} '.format(gravity['y']) +
              'Z={}'.format(gravity['z']))
        time.sleep(1)
