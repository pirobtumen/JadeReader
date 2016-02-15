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
# Reader Entry
#-------------------------------------------------------------------------------

class ReaderEntry:
	"""
	Object that contains ReaderEntry's data:
		- Name
		- URL
        - Category
	"""
	def __init__(self, data ):
		self.data = data

	def get_name(self):
		return self.data[ 0 ]

	def get_url(self):
		return self.data[ 1 ]

	def get_category(self):
		return self.data[2]

	def get_data(self):
		return self.data

	def set_category(self, new):
		self.data[2] = new

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
			return [obj.get_name(), obj.get_url(), obj.get_category()]

		# Let the base class default method raises the TypeError
		return json.JSONEncoder.default(self, obj)


#-------------------------------------------------------------------------------
# Reader Model
#-------------------------------------------------------------------------------

class ReaderDB:
	"""
	This object reads the data from a JSON file and adds it to a dictionary.

	In the dictionary each key has a val, a ReaderEntry that holds the URL info.

	CategoryDB provides a fast way to access all keys in one category.
	Each entry has a 'Category' attribute that is added (with the entry's key)
	to the "CategoryDB" object.

	So ReaderDB provides:

	- Fast access to each entry by its key.
	- Fast access to each category by its name.

	( Also other methods: set, get, delete, check... )

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

		# Get the data
		self.data = self.data_io.read()

		# Parse the data
		for key in self.data:
			# Create data
			entry = ReaderEntry( self.data[key] )
			self.data[key] = entry

			# Add the key-category
			self.categories.add_key_val( entry.get_category(), key )

	def save_data(self):
		"""
		Builds the JSON structure in a dictionary and saves it to disk.
		"""

		self.data_io.save( self.data )

	# Categories
	#---------------------------------------------------------------------------

	def check_category( self, name ):
		"""
		Checks if a category exists.

		Returns 'True' if it exists.
		"""
		return self.categories.check_key( name )

	def get_category_entries(self, category):
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

	def delete_category(self, category):
		"""
		Deletes a category and its elements.
		"""
		# TODO: Move to "Uncategorized"
		self.categories.del_key( category )

	def rename_category(self, old, new ):
		"""
		Renames a category.
		"""
		# Rename the category
		self.categories.rename( old, new )

		# Get the keys of this category
		keys = self.categories.get_key( new )

		# Update the categories
		for key in keys:
			self.data[key].set_category( new )

	# Web Entries
	#---------------------------------------------------------------------------

	def add(self, entry):
		"""
		Adds a new entry and it is appended to a category.
		"""
		# TODO: change key
		key = str(len(self.data))

		# Add the entry
		self.data[key] = entry

		# Add the category
		self.categories.add_key_val( entry.get_category(), key )

		return key

	def set(self, key, entry ):
		"""
		Updates a entry by its key.
		"""

		old_category = self.data[key].get_category()
		new_category = entry.get_category()

		if old_category != new_category:
			# Remove category key
			self.categories.del_key_val( old_category, key )

			# Add to the new category
			self.categories.add_key_val( new_category, key )

		# Update data
		self.data[key] = entry


	def get_all(self):
		"""
		Returns all the keys.
		"""
		return self.data.keys()

	def get(self, key):
		"""
		Returns the entry whose key is 'key'.
		"""
		return self.data[key]

	def delete(self, key):
		"""
		Deletes a key.
		If the category is empty it is also deleted.
		"""
		category = self.get(key).get_category()

		# Delete key from data
		del self.data[key]

		# Delete from its category
		return self.categories.del_key_val( category, key )
