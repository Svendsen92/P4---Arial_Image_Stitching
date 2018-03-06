"""
Database manager library.

Provides a class to interface with and sqlite3 database
that stores the images meta-data.

Created by Eduardo Ponz, Steffan Svendsen, Vincent Joly,
David Michalik, Ivelin Penchev & Simone Jensen.
4th semester, Bachelor in Robotics, AAU. 13-feb-2018.
"""

import os
import sqlite3

from time import gmtime, strftime


class DatabaseManager():
	"""."""

	def __init__(self):
		"""."""
		self.TABLE_NAME = 'meta-data'
		self.COLUMN_ID = 'id'
		self.COLUMN_JOB_ID = 'job_id'
		self.COLUMN_IMAGE_NAME = 'image_name'
		self.COLUMN_GRAVITY_X = 'gravity_x'
		self.COLUMN_GRAVITY_Y = 'gravity_y'
		self.COLUMN_GRAVITY_Z = 'gravity_z'
		self.COLUMN_HEADING = 'heading'
		self.COLUMN_ROLL = 'roll'
		self.COLUMN_PITCH = 'pitch'
		self.COLUMN_BLADE_DISTANCE = 'blade_distance'
		self.COLUMN_HEIGHT = 'height'
		
		db_path = os.path.dirname(__file__)
        db_path = os.path.abspath(os.path.join(db_path, os.pardir))
        db_path = os.path.abspath(os.path.join(db_path, "database"))
        db_path = os.path.abspath(os.path.join(db_path, "images_database.db"))
        print('Connecting to database. Database path: {}'.format(db_path))
        self.db = sqlite3.connect(db_path)
        print('Connected to database!')
        self.cursor = self.db.cursor()
        self.create_table_meta_data()

    def create_table_meta_data(self):
    	"""Create table_meta_data."""
        self.db.execute('CREATE TABLE IF NOT EXISTS ' + self.TABLE_NAME +
                        ' (' + self.COLUMN_ID +
                        ' INTEGER PRIMARY KEY AUTOINCREMENT, ' +
                        self.COLUMN_MACHINE_ID + ' TEXT NOT NULL, ' +
                        self.COLUMN_JOB_ID + ' TEXT NOT NULL, ' +
                        self.COLUMN_IMAGE_NAME + ' TEXT NOT NULL, ' +
                        self.COLUMN_GRAVITY_X + ' TEXT NOT NULL, ' +
                        self.COLUMN_GRAVITY_Y + ' TEXT NOT NULL, ' +
                        self.COLUMN_GRAVITY_Z + ' TEXT NOT NULL, ' +
                        self.COLUMN_HEADING + ' TEXT NOT NULL, ' +
                        self.COLUMN_ROLL + ' TEXT NOT NULL, ' +
                        self.COLUMN_PITCH + ' TEXT NOT NULL, ' +
                        self.COLUMN_BLADE_DISTANCE + ' TEXT NOT NULL, ' +
        				self.COLUMN_HEIGHT + ' TEXT NOT NULL)')

    def insert_meta_data(self, job_id, image_name, gravity_x, gravity_y,
    					 gravity_z, heading, roll, pitch, blade_distance,
    					 height):
    	"""."""
    	timestamp = strftime("%y-%m-%d%Z%H:%M:%S", gmtime())
    	params = (job_id, image_name, gravity_x, gravity_y, gravity_z,
    			  heading, roll, pitch, blade_distance, height, timestamp)
        self.db.execute('INSERT INTO ' + self.TABLE_NAME + ' (' +
                self.COLUMN_JOB_ID + ', ' +
                self.COLUMN_IMAGE_NAME + ', ' +
                self.COLUMN_GRAVITY_X + ', ' +
                self.COLUMN_GRAVITY_Y + ', ' +
                self.COLUMN_GRAVITY_Z + ', ' +
                self.COLUMN_HEADING + ', ' +
                self.COLUMN_ROLL + ', ' +
                self.COLUMN_PITCH + ', ' +
                self.COLUMN_BLADE_DISTANCE + ', ' +
                self.COLUMN_HEIGHT + ', ' +
                self.COLUMN_TIMESTAMP + ') ' +
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', params)
        self.db.commit()
