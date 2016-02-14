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
	def __init__(self, parent, title ):
		super(Gtk.Window,self).__init__( title="Jade Reader" )
		self.title = "Jade Reader - " + title
		self.set_default_size(700,400)
		self.connect("delete-event", self.close )

		# RSS URL
		self.rss_url = None

		# Load components
		self.load_components()

	def load_components(self):
		# Update header bar
		header_bar = Gtk.HeaderBar()
		header_bar.set_title( self.title )
		header_bar.set_subtitle("Reader")
		header_bar.set_show_close_button(True)

		# Change the Window's title bar
		self.set_titlebar( header_bar )

	def set_rss(self, rss ):
		self.rss_url = rss

	def close(self, window, widget):
		self.destroy()

	def run(self):
		if self.rss_url is not None:
			# Show components
			self.show_all()
