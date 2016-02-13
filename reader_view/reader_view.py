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
import webbrowser

#-------------------------------------------------------------------------------

class ReaderView( Gtk.Window ):
	def __init__(self, parent, entry_model ):
		super(Gtk.Window,self).__init__( title="Jade Reader - " + entry_model.get_name() )
		self.set_default_size(700,400)
		self.connect("delete-event", self.close )
		self.show_all()

	def close(self, window, event ):
		self.destroy()
