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

from gi.repository import Gtk
from model.reader import ReaderEntry

#-------------------------------------------------------------------------------

class EntryEditView( Gtk.Dialog ):
	def __init__(self, parent, categories, buttons=None):
		Gtk.Dialog.__init__(self, "URL Manager", parent, 0 )
		self.set_default_size(150, 100)

		label_name = Gtk.Label("Name:")
		self.name = Gtk.Entry()

		label_url = Gtk.Label("URL:")
		self.url = Gtk.Entry()

		label_cat = Gtk.Label("Category:")
		cat_list = Gtk.ListStore(str)

		for category in categories:
			cat_list.append( [category] )

		self.cat = Gtk.ComboBox.new_with_model_and_entry(cat_list)
		self.cat.set_entry_text_column(0)

		#self.cat.set_activates_default(True)

		main_box = self.get_content_area()

		grid = Gtk.Grid()
		#grid.set_row_homogeneous(True)
		grid.set_row_spacing(4)
		grid.set_column_spacing(4)

		grid.add( label_name )
		grid.attach_next_to( self.name, label_name,
		Gtk.PositionType.RIGHT, 2, 1 )

		grid.attach_next_to( label_url, label_name,
		Gtk.PositionType.BOTTOM, 1, 1 )

		grid.attach_next_to( self.url, label_url,
		Gtk.PositionType.RIGHT, 2, 1 )

		grid.attach_next_to( label_cat, label_url,
		Gtk.PositionType.BOTTOM, 1, 1 )

		grid.attach_next_to( self.cat, label_cat,
		Gtk.PositionType.RIGHT, 2, 1 )

		main_box.add( grid )

		super(Gtk.Dialog, self).add_button( "Cancel", Gtk.ResponseType.CANCEL )
		super(Gtk.Dialog, self).add_button( "Save", Gtk.ResponseType.OK )

		# Set as the default action
		ok_bttn = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
		ok_bttn.set_can_default(True)
		ok_bttn.grab_default()

	#---------------------------------------------------------------------------

	def set_name(self, name):
		self.name.set_text(name)

	#---------------------------------------------------------------------------

	def set_url(self, url):
		self.url.set_text(url)
	#---------------------------------------------------------------------------

	def set_category(self, category):
		cat_entry = self.cat.get_child()
		cat_entry.set_text( category )

	#---------------------------------------------------------------------------

	def run(self):
		self.show_all()
		result = super(Gtk.Dialog, self).run()

		web_entry = None
		category = None

		if result == Gtk.ResponseType.OK:
			web_entry = ReaderEntry( [ self.name.get_text(), self.url.get_text() ] )
			category = self.cat.get_child().get_text()

		self.destroy()

		return web_entry, category
