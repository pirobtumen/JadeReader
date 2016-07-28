"""
Copyright 2016 Alberto Sola

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class SourceRow(Gtk.ListBoxRow):
    def __init__(self,name,url,feed):
        super(Gtk.ListBoxRow, self).__init__()

        main_box = Gtk.VBox()

        main_box.add(Gtk.Label(name))
        main_box.add(Gtk.Label(url))
        main_box.add(Gtk.Label(str(feed)))

        button_box = Gtk.HBox()
        button_box.pack_start(Gtk.Button("Open"),False,False,0)
        button_box.pack_start(Gtk.Button("Enable"),False,False,0)
        button_box.pack_start(Gtk.Label(),True,True,0)
        button_box.pack_start(Gtk.Button("Edit"),False,False,0)

        main_box.add(button_box)
        self.add(main_box)
