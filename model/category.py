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

# Category DataBase
#-------------------------------------------------------------------------------

class CategoryDB:
	"""
	CategoryDB
	===================
	This object has a dictionary.
	Each key has a list of elements. Each element can be anything you need,
	for example, another list of values, a tuple, etc.
	"""

	#---------------------------------------------------------------------------

	def __init__(self):
		"""
		Initializes the attributes.
		"""
		self.key_data = {}

	#---------------------------------------------------------------------------
	# Data
	#---------------------------------------------------------------------------

	def get_data(self):
		"""
		Returns the internal data.
		"""
		return self.key_data

	def set_data(self, data):
		"""
		Sets the internal data.

		Param[in]: data
		"""
		self.key_data = json.loads( data )

	#---------------------------------------------------------------------------
	# Keys
	#---------------------------------------------------------------------------

	def add_key(self, name, data=[] ):
		"""
		Add a new key if it doesn't exists.

		Param[in]: name Key name
		Param[in]: data Data to add if the key doesn't exists. By default
		is an empty List.

		Return: True if the key has been added, False if not.
		"""
		can_add = not self.check_key(name)
		if can_add:
			self.key_data[name] = [data]

		return can_add

	def del_key(self, name):
		"""
		Deletes a key and its data.

		Param[in]: name Key name
		"""
		del self.key_data[name]

	def check_key(self, name):
		"""
		Checks if a key exists.

		Param[in]: name Key name

		Return: True if it exists, False if not.
		"""
		return name in self.key_data

	def get_key(self, name):
		"""
		Gets the data linked with its key.

		Param[in]: name Key name.

		Return: data holds by a key.
		"""
		return self.key_data.get(name, [])

	def get_all_keys(self):
		"""
		Return a list with all the Keys.
		"""
		return self.key_data.keys()


	#---------------------------------------------------------------------------
	#  Values
	#---------------------------------------------------------------------------

	def add_key_val(self, key, data ):
		"""
		Add a new value to the list that is associated with 'key'.

		Param[in]: data (to be added.)
		Param[in]: key Key value in the dictionary.
		"""

		if self.check_key( key ):
			self.get_key(key).append(data)
		else:
			self.add_key( key, data )

	def del_key_val(self, key, pos ):
		"""
		Deletes a element associated with a key. You need to specify the
		position of this element.

		Param[in]: key Key value in the dictionary.
		Param[in]: pos Value at position to be removed.
		"""
		if self.check_key( key ):
			data = self.get_key( key )
			if pos < len( data ):
				del data[pos]


	#---------------------------------------------------------------------------
	# Others
	#---------------------------------------------------------------------------

	def __str__(self):
		"""
		Returns the object as a String.
		"""
		return str(self.key_data)
