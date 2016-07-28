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

class FeedRow(Gtk.ListBoxRow):
    def __init__(self,title,data,url):
        super(Gtk.ListBoxRow, self).__init__()

        self.link = url

        main_box = Gtk.VBox()

        title_label = Gtk.Label(title)
        title_label.set_line_wrap(True)
        main_box.pack_start(Gtk.Label(title),True,True,0)

        data_label = Gtk.Label()
        data_label.set_text( data )
        data_label.set_line_wrap(True)

        main_box.pack_start(data_label,True,True,0)

        self.add(main_box)
