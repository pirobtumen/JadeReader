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

"""
Manager View
=======================

Simple, easy and modern Web Manager.

"""

# Imports
#-------------------------------------------------------------------------------

from gi.repository import Gtk
from gi.repository import Gio
import webbrowser

from manager_view.entry_view import EntryView
from manager_view.entry_edit_view import EntryEditView
from manager_view.inputdialog import InputDialog
from reader_view.reader_view import ReaderView
from model.reader import ReaderDB

import easyscrap

#-------------------------------------------------------------------------------

class ManagerView( Gtk.Window ):

	def __init__(self, reader_model ):
		super(Gtk.Window,self).__init__( title="Jade Reader" )
		self.set_default_size(700,400)
		self.reader = reader_model
		self.current_category = None
		self.load_components()
		self.connect("delete-event", Gtk.main_quit)
		self.show_all()

	#---------------------------------------------------------------------------
	# Components
	#---------------------------------------------------------------------------

	def load_components(self):

		# Header Bar
		self.set_header_bar()

		# Set containers
		self.set_window_containers()

		# Lateral menu
		self.set_lateral_menu_view()

		# Data view
		self.set_data_view()

		# Menu
		self.load_menu()

	#---------------------------------------------------------------------------

	def set_header_bar(self):
		# Header bar
		header_bar = Gtk.HeaderBar()
		header_bar.set_title("Jade Reader")
		header_bar.set_subtitle("Manager")
		header_bar.set_show_close_button(True)

		# Add URL button
		add_data_btn = Gtk.Button(label="Add")
		add_data_btn.connect("clicked", self.btn_add_url )
		header_bar.pack_start( add_data_btn )

		# Add a MenuButton
		menu_btn = Gtk.MenuButton(label="Menu")

		menumodel = Gio.Menu()
		menu_btn.set_menu_model(menumodel)
		menumodel.append("About", "None")

		header_bar.pack_end( menu_btn )

		# Change the Window's title bar
		self.set_titlebar( header_bar )

	#---------------------------------------------------------------------------

	def load_menu(self):
		# Categories Right-Click Menu
		self.cat_menu = Gtk.Menu()

		# Options
		rename = Gtk.MenuItem("Rename")
		rename.connect( "activate", self.rename_category )
		#delete = Gtk.MenuItem("Delete")
		#delete.connect( "activate", self.delete_category )

		# Add buttons
		self.cat_menu.append(rename)
		#self.cat_menu.append(delete)
		self.cat_menu.show_all()

	#---------------------------------------------------------------------------

	def set_window_containers(self):
		# Set the main window structure
		main_box = Gtk.Box( orientation=Gtk.Orientation.VERTICAL )

		# TODO: not used
		# A window Header
		self.header_box = Gtk.Box()

		# Main Window Content
		# TODO: Min width when resize left
		main_wrap = Gtk.Paned()

		# Add the sub-boxes to the main box
		main_box.pack_start( self.header_box, False, True, 0 )
		main_box.pack_start( main_wrap, True, True, 0 )

		self.menu_box = Gtk.Box( orientation=Gtk.Orientation.VERTICAL )
		self.menu_box.set_size_request(150,200)
		main_wrap.add1( self.menu_box )

		self.data_box = Gtk.Box( orientation=Gtk.Orientation.VERTICAL )
		self.data_box.set_size_request(350,300)
		main_wrap.add2( self.data_box )

		# Add the main box to the window
		self.add( main_box )

	#---------------------------------------------------------------------------

	def set_data_view(self):
		# Empty tree view
		self.scroll_tree = Gtk.ScrolledWindow()

		# Initial view
		self.show_all_entries(None)
		self.data_box.pack_start( self.scroll_tree, True, True, 0 )

	#---------------------------------------------------------------------------

	def set_lateral_menu_view(self):
		# DEFAULT MENU
		#-----------------------

		self.show_all_btn = Gtk.Button("Show all")
		self.show_all_btn.connect( "clicked", self.show_all_entries )

		# Add to the window
		self.menu_box.pack_start( self.show_all_btn, False, True, 0 )

		# CATEGORIES
		#-----------------------

		scroll_tree = Gtk.ScrolledWindow()

		categories_data = Gtk.ListStore( str )
		renderer = Gtk.CellRendererText()

		self.categories = Gtk.TreeView( categories_data )
		self.categories.connect('button-press-event' , self.category_selected)

		column = Gtk.TreeViewColumn("Categories", renderer, text=0)
		self.categories.append_column(column)

		scroll_tree.add( self.categories )
		self.menu_box.pack_start( scroll_tree,True,True,0 )

		# Load categories
		self.load_category_menu()

	#---------------------------------------------------------------------------
	# Actions
	#---------------------------------------------------------------------------

	def get_option_selected(self, treeview, event):
		category = None

		# Get row selectec by event coordinates
		row_selected = treeview.get_path_at_pos(int(event.x), int(event.y))

		# Get the treeview model
		model = treeview.get_model()

		# Check if there is not row selected
		if row_selected is not None:
			# Unpack the values
			path, col, x, y = row_selected

			# Get a model's iterator from path
			tree_iter = model.get_iter(path)

			# Get iterator value -> Category
			category = model.get_value(tree_iter,0)

		return category

	#---------------------------------------------------------------------------

	def category_selected(self, treeview, event):
		# Get the category selected
		category = self.get_option_selected( treeview, event )

		if category is not None:
			# Load the category
			if category != self.current_category:
				self.current_category = category
				self.load_category_entries( category )

			# Display menu
			if event.button == 3:
				self.cat_menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())

	#---------------------------------------------------------------------------

	def web_selected( self, list_view, entry ):
		# Get the EntryView and open the Reader
		if entry is not None:

			# Look for RSS
			scrap = easyscrap.EasyScrap( entry.get_url() )
			title, rss = scrap.get_rss_url()

			# If there isn't RSS open in Web Browser
			if rss is None:
				self.open_browser( entry.get_url() )
			else:
				url_view = ReaderView( self, entry.get_name() )
				url_view.set_rss( rss )
				url_view.run()

	#---------------------------------------------------------------------------

	def open_browser(self, url):
		# TODO: EasyScrap: URL is valid + Add scheme
		webbrowser.open_new_tab("http://" + url)

	#---------------------------------------------------------------------------

	def btn_add_url(self, widget):
		dialog = EntryEditView(self, self.reader.get_category_list() )

		web_entry = dialog.run()
		if web_entry != None:
			self.add_web_entry( web_entry )

	#---------------------------------------------------------------------------
	# Model / View Update
	#---------------------------------------------------------------------------

	def load_category_menu(self):
		# Save current category
		cur_cat = self.current_category

		# Get categories from reader
		categories_list = self.reader.get_category_list()

		# Get the TreeView model
		category_model = self.categories.get_model()
		category_model.clear()

		# Add the categories
		for i in categories_list:
			category_model.append( [i] )

		# Restore the current_category
		self.current_category = cur_cat

	#---------------------------------------------------------------------------

	def show_all_entries(self, button):
		# Set current category
		self.current_category = 0

		# Unselect categories
		selection = self.categories.get_selection()
		selection.unselect_all()

		# Create a new ListBox
		entries = Gtk.ListBox()
		entries.connect( "row-activated", self.web_selected )

		# Get all the keys from the model
		all_keys = self.reader.get_all()

		# Build and add each entry
		for key in all_keys:
			entry_view = EntryView(self, self.reader.get(key), key)
			entries.add( entry_view )

		# Update the view
		self.load_entries( entries )

	#---------------------------------------------------------------------------

	def load_category_entries(self, category):
		# Show all
		if category == 0:
			self.show_all_entries( None )

		else:
			# Create a new ListBox
			entries = Gtk.ListBox()
			entries.connect( "row-activated", self.web_selected )

			# Get the keys that belong to 'category'
			category_keys = self.reader.get_category_entries( category )

			# Build and add each entry
			for key in category_keys:
				data = self.reader.get( key )
				entries.add( EntryView(self,data,key) )

			# Update the view
			self.load_entries( entries )

	#---------------------------------------------------------------------------

	def load_entries(self, list_box):
		# Get the ListView
		child = self.scroll_tree.get_child()

		# Remove its child
		if child != None:
			self.scroll_tree.remove( child )

		# Add the new list
		self.scroll_tree.add( list_box )
		self.scroll_tree.show_all()

	#---------------------------------------------------------------------------

	def rename_category(self, widget):
		# Renames the current category
		input_dialog = InputDialog( self, "New name" )

		# Get the new name
		new_category = input_dialog.show()

		# Rename and show categories
		if new_category is not None:
			self.reader.rename_category( self.current_category, new_category )
			self.load_category_menu()

			# Save data
			self.reader.save_data()

	#---------------------------------------------------------------------------

	#def delete_category(self, widget):
		# Delete all the entries in the current category.

	#---------------------------------------------------------------------------

	def add_web_entry(self, entry):
		# Check if the entry is valid
		if entry.valid():
			# Update categories if neccesary
			if not self.reader.check_category(entry.get_category()):
				model = self.categories.get_model()
				model.append( [entry.get_category()] )

			# Update model
			key = self.reader.add( entry )

			# Update the view
			# TODO 1: Optimize add - not reload all
			# TODO 1.1: Add the key given by the model to the WebEntryView
			self.load_category_entries( self.current_category )

		# Save data
		self.reader.save_data()

	def del_web_entry(self, key):
		# Delete the entry by its key
		category_empty = self.reader.delete(key)

		# Update category menu
		if category_empty:
			self.load_category_menu()

		# Update the view
		self.load_category_entries( self.current_category )

		# Save data
		self.reader.save_data()

		#---------------------------------------------------------------------------

	def edit_web_entry(self, key, entry):
		# Create the dialog
		dialog = EntryEditView(self, self.reader.get_category_list() )

		# Set the data
		dialog.set_name( entry.get_name() )
		dialog.set_url( entry.get_url() )
		dialog.set_category( entry.get_category() )

		# Get the user input
		web_entry = dialog.run()

		if web_entry != None:
			# Update entry
			self.reader.set( key, web_entry )

			# Update categories
			self.load_category_menu()

			# Update current category
			self.load_category_entries( self.current_category )

			# Save data
			self.reader.save_data()
