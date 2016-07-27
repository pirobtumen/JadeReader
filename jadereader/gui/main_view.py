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

class JadeReaderView(Gtk.Window):

    def __init__(self,url_manager):
        Gtk.Window.__init__(self, title="Jade Reader")

        # Attributes
        # --------------------
        self.url_manager = url_manager
        self.current_category = None

        # Events
        # --------------------
        self.connect("delete-event", Gtk.main_quit )

        # Widgets
        # --------------------
        hpane_main = Gtk.HPaned()
        self.add(hpane_main)
        self.set_lateral_menu(hpane_main)

        # Initialize
        # --------------------

        self.load_categories( url_manager.get_categories() )

        self.show_all()
        Gtk.main()

    def set_lateral_menu(self, container):
        # Lateral menu container
        # --------------------
        lateral_menu_box = Gtk.VBox()

        # Default options menu
        # --------------------
        default_menu_options_store = Gtk.ListStore(str)
        default_menu_options_store.append(["All sites"])

        default_menu_options = Gtk.TreeView(default_menu_options_store)

        renderer = Gtk.CellRendererText()
        option_name = Gtk.TreeViewColumn("Menu", renderer, text=0)
        default_menu_options.append_column(option_name)

        # Categories menu
        # --------------------
        self.category_menu_store = Gtk.ListStore(str)
        category_menu = Gtk.TreeView(self.category_menu_store)

        category_name = Gtk.TreeViewColumn("Categories",renderer, text=0)
        category_menu.append_column(category_name)

        # Add to the container
        # --------------------
        lateral_menu_box.pack_start(default_menu_options,False,False,0)
        lateral_menu_box.pack_start(category_menu,True,True,0)
        container.add1(lateral_menu_box)
        container.add2(Gtk.Label('Test'))


    # --------------------------------------------------------------------------

    def load_categories(self, categories_list):

        self.category_menu_store.clear()

        for category in categories_list:
            self.category_menu_store.append( [category] )

    #def load_feed(self, feed):

    #def load_source(self, source):
