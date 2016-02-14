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
Reader View
=======================

(...)

"""

# Imports
#-------------------------------------------------------------------------------

from gi.repository import Gtk
import webbrowser

from manager_view.entry_view import EntryView
from manager_view.entry_edit_view import EntryEditView
from reader_view.reader_view import ReaderView
from model.reader import ReaderDB

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
		header_bar.set_subtitle("Web Manager")
		header_bar.set_show_close_button(True)

		# Add URL button
		add_data_btn = Gtk.Button(label="Add")
		add_data_btn.connect("clicked", self.btn_add_url )
		header_bar.pack_start( add_data_btn )

		# Add a MenuButton
		menu_btn = Gtk.MenuButton(label="Menu")
		menu_btn.connect("clicked", self.btn_menu )
		header_bar.pack_end( menu_btn )

		# TODO: Menu Button
		# - Search
		# - Config

		# Change the Window's title bar
		self.set_titlebar( header_bar )

	#---------------------------------------------------------------------------

	def load_menu(self):
		# Categories Right-Click Menu
		self.cat_menu = Gtk.Menu()
		i1 = Gtk.MenuItem("Rename")
		self.cat_menu.append(i1)
		i2 = Gtk.MenuItem("Delete")
		self.cat_menu.append(i2)
		self.cat_menu.show_all()

	#---------------------------------------------------------------------------

	def set_window_containers(self):
		# Set the main window structure
		main_box = Gtk.Box( orientation=Gtk.Orientation.VERTICAL )

		# TODO: not used
		# A window Header
		self.header_box = Gtk.Box()

		# Main Window Content
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

		# TODO: Add initial view

		self.data_box.pack_start( self.scroll_tree, True, True, 0 )

	#---------------------------------------------------------------------------

	def set_lateral_menu_view(self):
		# TODO: Tree view -> Show all, Favs...

		# Categories tree view

		scroll_tree = Gtk.ScrolledWindow()
		#scroll_tree.set_size_request( 0, 300 )

		categories_data = Gtk.ListStore( str )

		self.categories = Gtk.TreeView( categories_data )
		self.categories.set_headers_visible(False)
		self.categories.connect('button-press-event' , self.category_selected)

		renderer = Gtk.CellRendererText()

		column = Gtk.TreeViewColumn("Categories", renderer, text=0)
		self.categories.append_column(column)

		scroll_tree.add( self.categories )
		self.menu_box.pack_start( scroll_tree,True,True,0 )
		#self.menu_box.pack_start( scroll_tree,False,True,0 )

		self.load_category_menu()

	#---------------------------------------------------------------------------
	# Actions
	#---------------------------------------------------------------------------

	def category_selected(self, treeview, event):
		row_selected = treeview.get_path_at_pos(int(event.x), int(event.y))
		model = treeview.get_model()

		if row_selected is not None:
			path, col, x, y = row_selected

			tree_iter = model.get_iter(path)
			category = model.get_value(tree_iter,0)

			self.current_category = category
			self.load_category_entries( category )

			# Display menu
			if event.button == 3:
				# TODO: Send name
				self.cat_menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())

	#---------------------------------------------------------------------------

	def web_selected( self, list_view, entry ):
		# TODO: create a window
		if entry != None:
			url = entry.get_url()
			url_view = ReaderView( self, entry )

	#---------------------------------------------------------------------------

	def open_browser(self, url):
		print( "Opening: " + url )
		webbrowser.open_new_tab("http://" + url)

	#---------------------------------------------------------------------------

	def btn_add_url(self, widget):
		dialog = EntryEditView(self, self.reader.get_category_list() )

		web_entry, category = dialog.run()
		if web_entry != None:
			self.add_web_entry( web_entry, category )

	#---------------------------------------------------------------------------

	def btn_menu(self, widget):
		# TODO: Load Menu
		print( "Load menu... ")

	#---------------------------------------------------------------------------
	# Model / View Update
	#---------------------------------------------------------------------------

	"""
	def show_all(self):
		pass

	show_about()

	show_info()

	"""

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

	def load_category_entries(self, category):

		category_keys = self.reader.get_category( category )
		new_list = Gtk.ListBox()

		for key in category_keys:
			data = self.reader.get( key )
			new_list.add( EntryView(self,data,key) )

		child = self.scroll_tree.get_child()

		if child != None:
			self.scroll_tree.remove( child )

		self.scroll_tree.add( new_list )
		self.scroll_tree.show_all()

		new_list.connect( "row-activated", self.web_selected )

	#---------------------------------------------------------------------------

	def add_category_to_menu(self, name):

		if not self.reader.check_category(name):
			model = self.categories.get_model()
			model.append( [name] )

	#---------------------------------------------------------------------------

	def add_web_entry(self, web_entry, category):
		if web_entry.valid():
			# Update categories if neccesary
			self.add_category_to_menu( category )

			# Update model
			key = self.reader.add( web_entry, category )

			# Update the view
			# TODO 1: Optimize add - not reload all
			# TODO 1.1: Add the key given by the model to the WebEntryView
			self.load_category_entries( self.current_category )

		# Save data
		self.reader.save_data()

	def del_web_entry(self, key):
		# Delete the entry by its key
		category_empty = self.reader.delete_category_element( self.current_category, key )

		# Update category menu
		if category_empty:
			self.load_category_menu()

		# Update the view
		self.load_category_entries( self.current_category )

		# Save data
		self.reader.save_data()

		#---------------------------------------------------------------------------

	def edit_web_entry(self, key, entry):
		dialog = EntryEditView(self, self.reader.get_category_list() )

		dialog.set_name( entry.get_name() )
		dialog.set_url( entry.get_url() )
		dialog.set_category( self.current_category )

		web_entry, category = dialog.run()
		if web_entry != None:
			# Update entry
			self.reader.update( key, web_entry, self.current_category, category )

			# Update categories
			self.load_category_menu()

			# Update current category
			self.load_category_entries( self.current_category )

			# Save data
			self.reader.save_data()
