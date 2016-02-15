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

from reader_view.reader_entry import ReaderEntryView

#-------------------------------------------------------------------------------

class ReaderView( Gtk.Window ):
	def __init__(self, parent, title, feed ):
		super(Gtk.Window,self).__init__( title="Jade Reader" )
		self.set_default_size(700,400)
		self.connect("delete-event", self.close )

		# Load components
		self.load_components("Jade Reader - " + title)

		# Parse feed data
		self.parse_feed( feed )

		# Show all
		self.show_all()

	def load_components(self, title):
		# Update header bar
		header_bar = Gtk.HeaderBar()
		header_bar.set_title( title )
		header_bar.set_subtitle("Reader")
		header_bar.set_show_close_button(True)

		# Change the Window's title bar
		self.set_titlebar( header_bar )

		# Scroll Widget
		self.scroll = Gtk.ScrolledWindow()

		# Add a ListBox for news
		reader_list = Gtk.ListBox()

		self.scroll.add( reader_list )
		self.add( self.scroll )

	def close(self, window, widget):
		self.destroy()

	def parse_feed(self, feed):

		reader_list = Gtk.ListBox()

		for entry in feed.entries:

			entry_view = ReaderEntryView()
			entry_view.set_title( entry.title )
			entry_view.set_data( entry.summary )

			reader_list.add(entry_view)
			reader_list.add( Gtk.Separator() )

		self.set_entries( reader_list )

	def set_entries(self, reader_list):
		# Get the ListView
		child = self.scroll.get_child()

		self.scroll.remove( child )

		# Add the new list
		self.scroll.add( reader_list )
