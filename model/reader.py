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

Author: Alberto Sola - 2016
"""

# Imports
#-------------------------------------------------------------------------------

import json

from category import CategoryDB
from file_io import FileIO

#-------------------------------------------------------------------------------
# Reader Model
#-------------------------------------------------------------------------------

class ReaderDB:
	def __init__( self, file_name ):

		self.data_io = FileIO( file_name, ReaderEntryJSON )
		self.data = self.data_io.read()
		self.categories = CategoryDB()
		self.parse_data()

	def parse_data(self):
		for key in self.data:
			# ReaderEntry
			entry = self.data[key]
			reader_entry = ReaderEntry( entry )

			# Update
			self.data[key] = reader_entry
			self.update_category( reader_entry.get_category(), key )

	# Categories
	#---------------------------------------------------------------------------

	def check_category( self, name ):
		return self.categories.check_key( name )

	def get_category(self, category):
		return self.categories.get_key(category)

	def get_category_list(self):
		return self.categories.get_all_keys()

	def update_category(self, category, key):
		# Add the category and data
		self.categories.add_key_val( category, key )

	# Web Entries
	#---------------------------------------------------------------------------

	def add(self, obj):
		# TODO: change key
		key = str(len(self.data))
		self.data[key] = obj

		self.update_category( obj.get_category(), key )

		self.data_io.save( self.data )

		return key

	#def remove(self, key):

	def get(self, key):
		return self.data[key]

	def set(self, key, obj):
		self.data[key] = obj

#-------------------------------------------------------------------------------
# ReaderEntry
#-------------------------------------------------------------------------------

class ReaderEntry:
	# Class data variables
	name_pos = 0
	url_pos = 1
	cat_pos = 2

	def __init__(self, data ):
		self.data = data

	def get_name(self):
		return self.data[ self.name_pos ]

	def get_url(self):
		return self.data[ self.url_pos ]

	def get_category(self):
		return self.data[ self.cat_pos ]

	def valid(self):
		# TODO: validate data
		return True


class ReaderEntryJSON( json.JSONEncoder ):
	def default(self, obj):
		if isinstance(obj, ReaderEntry):
			return [obj.get_name(), obj.get_url(), obj.get_category()]

		# Let the base class default method raises the TypeError
		return json.JSONEncoder.default(self, obj)
