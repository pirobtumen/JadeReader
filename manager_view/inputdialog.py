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

from gi.repository import Gtk

class InputDialog( Gtk.Dialog ):
    def __init__(self, parent, title, flags=Gtk.DialogFlags.MODAL):
        Gtk.Dialog.__init__(self, title, parent, flags)

        # Entry
        self.txt_input = Gtk.Entry()

        # Buttons
        cancel_btn = Gtk.Button("Cancel")
        self.add_action_widget( cancel_btn, Gtk.ResponseType.CANCEL )

        ok_btn = Gtk.Button("OK")
        self.add_action_widget( ok_btn, Gtk.ResponseType.OK )

        #Containers
        vbox = self.get_content_area()
        vbox.pack_start( self.txt_input, True, True, 0 )

        # Let the entry activate when "Enter" is pressed
        self.txt_input.set_activates_default(True)

        # Make 'OK' button the default action
        ok_btn.set_can_default(True)
        ok_btn.grab_default()

    def show(self, destroy=True):
        data = None

        # Show dialog
        self.show_all()

        # Get response
        response = self.run()

        if response == Gtk.ResponseType.OK:
            data = self.txt_input.get_text()

        # Destroy/Hide the dialog
        if destroy:
            self.destroy()
        else:
            self.hide()

        return data
