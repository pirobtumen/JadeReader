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

class ReaderEntryView( Gtk.ListBoxRow ):
    def __init__(self):
        Gtk.ListBoxRow.__init__(self)

        self.url = None

        # Load components
        self.load_components()

        # Show components
        self.show_all()

    def load_components(self):
        vbox = Gtk.Box( orientation=Gtk.Orientation.VERTICAL, spacing=20 )

        self.data = Gtk.Label( xalign=0 )
        self.data.set_line_wrap(True)

        hbox = Gtk.Box()

        self.title = Gtk.Label( xalign=0 )
        self.title.set_line_wrap(True)
        open_btn = Gtk.Button("Open")

        hbox.pack_start( self.title, True, True, 0 )
        hbox.pack_start( open_btn, False, True, 0 )

        vbox.pack_start( hbox, True, True, 0 )
        vbox.pack_start( self.data, True, True, 0 )

        self.add( vbox )

    def set_title(self, title):
        self.title.set_text( title )

    def set_data(self, data):
        self.data.set_text( data )

    def set_url(self, url):
        self.url = url

    #def open_web(self):
