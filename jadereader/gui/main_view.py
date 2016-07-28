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
from gi.repository import Gio

from gui.lateral_menu_view import LateralMenu
from gui.source_row_view import SourceRow
from gui.feed_row_view import FeedRow

from src.url.urlmanager import UrlManager
from src.feed.feedmanager import FeedManager

class JadeReaderView(Gtk.Window):

    def __init__(self,url_manager):
        Gtk.Window.__init__(self, title="Jade Reader")

        self.resize(500,300)

        # Attributes
        # --------------------
        self.url_manager = url_manager
        self.show_feed = True

        # Events
        # --------------------
        self.connect("delete-event", Gtk.main_quit )

        # Widgets
        # --------------------
        hpane_main = Gtk.HPaned()
        self.add(hpane_main)

        self.lateral_menu = LateralMenu(self)
        hpane_main.add1(self.lateral_menu)

        self.set_main_widgets(hpane_main)

        # Initialize
        # --------------------
        self.load_categories( url_manager.get_categories() )

        self.show_all()
        Gtk.main()

    def set_main_widgets(self, container):
        main_box = Gtk.VBox()

        # Action Bar
        action_bar = Gtk.ActionBar()
        swap_feed_source_bttn = Gtk.Button("Sources")
        swap_feed_source_bttn.connect("clicked", self.swap_feed_source_bttn)
        action_bar.add(swap_feed_source_bttn)

        #action_bar.add(Gtk.Label("Category:"))
        #action_bar.add(Gtk.ComboBox.new_with_entry())
        #action_bar.add(Gtk.Label("Site:"))
        #action_bar.add(Gtk.ComboBox.new_with_entry())

        # ListBox
        self.scrolled_window = Gtk.ScrolledWindow()

        # Add to the view
        main_box.pack_start(action_bar,False,False,0)
        main_box.pack_start(self.scrolled_window,True,True,0)

        container.add2(main_box)


    # --------------------------------------------------------------------------

    def load_categories(self, categories_list):

        self.lateral_menu.clear()

        for category in categories_list:
            self.lateral_menu.add_category(category)

    def load_data(self, option_selected):

        if option_selected == LateralMenu.OPTION_NONE:
            # TODO:
            pass

        elif option_selected == LateralMenu.OPTION_ABOUT:
            pass

        elif self.show_feed:
            self.load_feed(option_selected)

        else:
            self.load_source(option_selected)

        self.show_all()


    def load_feed(self, option_selected):
        feed_manager = FeedManager()

        scrolled_window_child = self.scrolled_window.get_child()
        if scrolled_window_child is not None:
            self.scrolled_window.remove( scrolled_window_child )

        data_listbox = Gtk.ListBox()

        if option_selected == LateralMenu.OPTION_ALL:
            # TODO: get_all()
            categories = self.url_manager.get_categories()
            source_list = []

            for category in categories:
                source_list += self.url_manager.get_category(category)

        else:
            source_list = self.url_manager.get_category(option_selected)

        feed_list = feed_manager.download_feed(source_list)

        for feed in feed_list:
            data_listbox.add( FeedRow(feed.get_title(), feed.get_data(), feed.get_link()) )

        self.scrolled_window.add(data_listbox)

    def load_source(self, option_selected):

        scrolled_window_child = self.scrolled_window.get_child()
        if scrolled_window_child is not None:
            self.scrolled_window.remove( scrolled_window_child )

        data_listbox = Gtk.ListBox()

        if option_selected == LateralMenu.OPTION_ALL:
            # TODO: get_all()
            categories = self.url_manager.get_categories()
            source_list = []

            for category in categories:
                source_list += self.url_manager.get_category(category)

        else:
            source_list = self.url_manager.get_category(option_selected)

        for source in source_list:
            data_listbox.add( SourceRow(source.get_name(), source.get_url(), source.get_feed() ) )

        self.scrolled_window.add(data_listbox)

    def swap_feed_source_bttn(self,button):
        self.show_feed = not self.show_feed

        if self.show_feed:
            button.set_label("Sources")
        else:
            button.set_label("Feed")

        self.load_data( self.lateral_menu.get_option_selected() )
