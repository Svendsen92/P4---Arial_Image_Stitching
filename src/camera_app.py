import os

from lib.database_manager import DatabaseManager
from lib.Image_manager import image_manager
from lib.imu import ImuReader
from lib.Lidar import lidar
from lib.logger import Logger
from lib.gps import GPS_Reader

def drone_signal():
	input()
	return True

def drone_next_position():
	print("Going to next position")


if __name__ == '__main__':
	file_path = os.path.dirname(__file__)
    file_path = os.path.abspath(os.path.join(file_path, "log.log"))
	log = Logger(file_path)
	log.log('Initializing objects', level=1, days_to_remain=5)
	imu = ImuReader()
	lidar = lidar()
	image_manager = image_manager()
	db_manager = DatabaseManager()
	gps = GPS_Reader()
	savePath = os.path.dirname(__file__)
	picID = "test_"
	iteration = 1
	log.log('Objects successfully initialized', level=1, days_to_remain=5)

	while True:

		if drone_signal() is True:
			log.log('Drone signal received', level=1, days_to_remain=5)
			status = image_manager.aquirePicture(picID, savePath, iteration)['status']

			while not status:
				status = image_manager.aquirePicture(picID, savePath, iteration)['status']
				log.log('Image not successfully acquired', level=2, days_to_remain=5)

			log.log('Image successfully acquired', level=2, days_to_remain=5)
			log.log('Getting sensor data', level=1, days_to_remain=5)
			gravity = imu.get_gravity()
			euler = imu.get_euler()
			distance = lidar.distance()
			height = gps.get_position()['z']
			image_name = image_manager.aquirePicture()['name']
			log.log('Sensor data acquired', level=1, days_to_remain=5)

			insert_meta_data(1, image_name, gravity['x'], gravity['y'],
    					 gravity['z'], euler['heading'], euler['roll'],
    					 euler['pitch'], distance, height)
			log.log('Meta data stored in the database', level=2, days_to_remain=5)
			iteration +1

			drone_next_position()
			log.log('Sending drone to next position', level=2, days_to_remain=5)
