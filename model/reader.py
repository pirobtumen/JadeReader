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

"""
	ReaderDB ( model )
=========================

(...)

"""

# Imports
#-------------------------------------------------------------------------------

import json

from model.category import CategoryDB
from model.file_io import FileIO

#-------------------------------------------------------------------------------
# Reader Model
#-------------------------------------------------------------------------------

class ReaderDB:
	"""
	ReaderDB

	(...)
	"""
	def __init__( self, data_fname="data.json" ):
		# File I/O
		self.data_io = FileIO( data_fname, ReaderEntryJSON )

		# Data
		self.categories = CategoryDB()
		self.data = {}

		# Get the data
		self.read_data()

	# Data IO
	#---------------------------------------------------------------------------

	def read_data(self):
		"""
		Reads the data from the JSON file and parses the entries
		and the categories.
		"""
		# Default structure if the file is empty
		data = { "data" : {}, "categories" : {} }

		# Get the data
		data = self.data_io.read( data )

		# Set the data
		self.data = data["data"]
		self.categories.set_data( data["categories"] )

		# Parse the data
		for key in self.data:
			# ReaderEntry
			entry = self.data[key]
			reader_entry = ReaderEntry( entry )

			# Update
			self.data[key] = reader_entry

	def save_data(self):
		"""
		Builds the JSON structure in a dictionary and saves it to disk.
		"""
		data = {}

		data["data"] = self.data
		data["categories"] = self.categories.get_data()

		self.data_io.save( data )

	# Categories
	#---------------------------------------------------------------------------

	def check_category( self, name ):
		"""
		Checks if a category exists.

		Returns 'True' if it exists.
		"""
		return self.categories.check_key( name )

	def get_category(self, category):
		"""
		Returns the keys that belong to a certain category.

		Param[in]: category
		"""
		return self.categories.get_key(category)

	def get_category_list(self):
		"""
		Returns a list with all the categories.
		"""
		return self.categories.get_all_keys()

	def update_category(self, category, key):
		"""
		Adds a new category ( if it doesn't exist ) and appends
		the key to that category.
		"""
		# Add the category and data
		self.categories.add_key_val( category, key )

	def delete_category_element(self, category, key):
		"""
		Deletes a key in a category. If the category is empty it is
		also deleted.
		"""
		data = self.categories.get_key( category )
		pos = 0

		# Delete key from data
		del self.data[key]

		# Delete from its category
		for element in data:
			if element == key:
				self.categories.del_key_val( category, pos )
			pos += 1

		# Check if category is empty
		data_empty = not data
		if data_empty:
			self.delete_category( category )

		return data_empty

	def delete_category(self, category):
		"""
		Deletes a category and its elements.
		"""
		self.categories.del_key( category )

	# Web Entries
	#---------------------------------------------------------------------------

	def add(self, entry, category):
		"""
		Adds a new entry and it is appended to a category.
		"""
		# TODO: change key
		key = str(len(self.data))

		# Add the entry
		self.data[key] = entry

		# Add the category
		self.update_category( category, key )

		return key

	def update(self, key, entry, old_category, new_category):
		"""
		Updates a entry (by its key) and its category.
		"""

		if old_category != new_category:
			# Remove category key
			self.delete_category_element( old_category, key )

			# Add to the new category
			self.update_category( new_category, key )

		# Update data
		self.data[key] = entry


	def get(self, key):
		"""
		Returns the entry whose key is 'key'.
		"""
		return self.data[key]

	def delete(self, key):
		"""
		Deletes the key 'key' and its data.
		"""
		del self.data[key]

#-------------------------------------------------------------------------------
# ReaderEntry
#-------------------------------------------------------------------------------

class ReaderEntry:
	"""
	Object that contains ReaderEntry's data:
		- Name
		- URL
	"""
	def __init__(self, data ):
		self.data = data

	def get_name(self):
		return self.data[ 0 ]

	def get_url(self):
		return self.data[ 1 ]

	def get_data(self):
		return self.data

	def valid(self):
		# TODO: validate data
		return True


class ReaderEntryJSON( json.JSONEncoder ):
	"""
	Custom JSON Encoder for a Reader Entry.
	"""
	def default(self, obj):
		# Check if 'obj' is a ReaderEntry
		if isinstance(obj, ReaderEntry):
			return [obj.get_name(), obj.get_url()]

		# Let the base class default method raises the TypeError
		return json.JSONEncoder.default(self, obj)
