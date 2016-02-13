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

#-------------------------------------------------------------------------------

class EntryView(Gtk.ListBoxRow):
	def __init__( self, parent, data, key ):
		Gtk.ListBoxRow.__init__(self)

		self.parent = parent
		self.entry = data
		self.key = key

		logo = Gtk.Label("Icon", valign=Gtk.Align.CENTER )
		name = Gtk.Label( self.entry.get_name() )
		url = Gtk.Label( self.entry.get_url() )

		edit_btn = Gtk.Button("Edit")
		edit_btn.connect( "clicked", self.btn_edit_entry )

		delete_btn = Gtk.Button("Delete")
		delete_btn.connect( "clicked", self.btn_del_entry )

		# Row Container
		hbox = Gtk.Box(spacing=50)

		# Add the Icon
		hbox.pack_start( logo, False, True, 10 )

		# Add the URL data
		vbox = Gtk.Box( orientation=Gtk.Orientation.VERTICAL )
		vbox.pack_start( name, True, True, 0 )
		vbox.pack_start( url, True, True, 0 )
		hbox.pack_start(vbox, True, True, 0 )

		# Buttons Box
		btn_hbox = Gtk.Box()
		hbox.pack_start( btn_hbox, False, True, 0 )

		btn_hbox.pack_start( edit_btn, False, True, 0 )
		btn_hbox.pack_start( delete_btn, False, True, 0 )

		self.add(hbox)
		self.show_all()

	def get_url(self):
		return self.entry.get_url()

	def get_name(self):
		return self.entry.get_name()

	def get_entry(self):
		return self.entry

	def btn_del_entry(self, button):
		self.parent.del_web_entry( self.key )

	def btn_edit_entry(self, button):
		self.parent.edit_web_entry( self.key, self.entry )
