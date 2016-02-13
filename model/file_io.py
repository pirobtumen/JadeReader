"""
Copyright (C) 2016  Alberto Sola

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Imports
#-------------------------------------------------------------------------------

import os
import json

# File Input / Output
#-------------------------------------------------------------------------------

class FileIO:
	"""
	FileIO
	=====================

	(...)

	"""

	def __init__(self, file_name, encoder=None):
		"""
			Initializes the object reading the file.
			If the file doesn't exist it creates a new one
			and add some default keys.

			Param[in]: file_name String with the file name.
			Param[in]: def_keys 'Default keys' if the file doesn't exists.
		"""
		self.encoder = encoder
		self.data_file_name = file_name

	#---------------------------------------------------------------------------
	# File I/O
	#---------------------------------------------------------------------------

	def check_file(self):
		return os.path.exists( self.data_file_name )

	def delete(self):
		"""
		Deletes the file associated with this object.
		"""
		os.remove( self.data_file_name )

	def read(self, default_data=None):
		"""
		Reads the data from the file and updates the object.

		param[in]: default_data  If the file is empty, this structure is going
		to be written to disk.
		"""

		print("\nReading data from config file: " + self.data_file_name)

		data = {}

		# If the file exists
		if self.check_file():
			# Get the data
			with open( self.data_file_name, 'r') as file_data:
				content = file_data.read()

			# Parse JSON
			data = json.loads( content )

		# Create a new empty file
		elif default_data is not None:
			self.save( default_data )
			data = default_data
		else:
			self.save( data )

		return data

	#---------------------------------------------------------------------------

	def save(self, data):
		"""
		Updates the file with the object data.
		"""
		print("\nSaving data to file: " + self.data_file_name)

		# Open the file
		file_data = open( self.data_file_name, 'w' )
		file_data.write( json.dumps( data, cls=self.encoder ) )
		file_data.close()

	#---------------------------------------------------------------------------

	def clear(self):
		"""
		Deletes all categories and data.
		"""
		self.key_data.clear()
		self.save()
