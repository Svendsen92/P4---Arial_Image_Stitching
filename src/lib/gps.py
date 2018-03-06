class GPS_Reader:

	def __init__(self):
		self.position = {}
		

	def get_position(self):

		self.position['x'] = 4
		self.position['y'] = 5
		self.position['z'] = 2.5		
		return self.position
