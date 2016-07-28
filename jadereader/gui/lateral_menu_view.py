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

class LateralMenu(Gtk.VBox):

    OPTION_NONE = 0
    OPTION_ALL = 1
    OPTION_ABOUT = 2

    def __init__(self, parent):
        super(Gtk.VBox, self).__init__()

        self.parent = parent
        self.option_selected = self.OPTION_NONE

        renderer = Gtk.CellRendererText()

        # Default options menu
        # --------------------

        # Problem -> Always the first row is autoselected

        default_menu_options_store = Gtk.ListStore(str)
        default_menu_options_store.append(["All"])
        default_menu_options_store.append(["About"])

        default_menu_options = Gtk.TreeView(default_menu_options_store)
        option_name = Gtk.TreeViewColumn("Menu", renderer, text=0)
        default_menu_options.append_column(option_name)

        self.default_menu_options_selection = default_menu_options.get_selection()
        self.default_menu_options_selection.connect("changed",self.option_selected_action)

        # Categories menu
        # --------------------
        self.category_menu_store = Gtk.ListStore(str)
        category_menu = Gtk.TreeView(self.category_menu_store)
        self.category_menu_selection = category_menu.get_selection()
        self.category_menu_selection.connect("changed",self.category_selected_action)

        category_name = Gtk.TreeViewColumn("Categories",renderer, text=0)
        category_menu.append_column(category_name)

        # Add to the container
        # --------------------
        self.pack_start(default_menu_options,False,False,0)
        self.pack_start(category_menu,True,True,0)


    def option_selected_action(self,selection):

        treeModel, treeIter = selection.get_selected()
        if treeIter != None:
            option = treeModel[treeIter][0]
            self.category_menu_selection.unselect_all()

            if option == "All":
                self.option_selected = self.OPTION_ALL

            elif option == "About":
                self.option_selected = self.OPTION_ABOUT

            self.parent.load_data(self.option_selected)


    def category_selected_action(self,selection):

        treeModel, treeIter = selection.get_selected()
        if treeIter != None:
            self.default_menu_options_selection.unselect_all()

            self.option_selected = treeModel[treeIter][0]

            self.parent.load_data(self.option_selected)

    def get_option_selected(self):
        return self.option_selected

    def add_category(self,category):
        self.category_menu_store.append([category])

    def clear(self):
        self.category_menu_store.clear()
