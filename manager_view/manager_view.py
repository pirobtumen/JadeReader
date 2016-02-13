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
		# Set containers
		self.set_window_containers()

		# Toolbox
		self.set_toolbox_view()

		# Lateral menu
		self.set_lateral_menu_view()

		# Data view
		self.set_data_view()

	#---------------------------------------------------------------------------

	def set_window_containers(self):
		# Set the main window structure
		main_box = Gtk.Box( orientation=Gtk.Orientation.VERTICAL )
		self.tool_box = Gtk.Box()

		main_wrap = Gtk.Box()

		# Add the sub-boxes to the main box
		main_box.pack_start( self.tool_box, False, True, 0 )
		main_box.pack_start( main_wrap, True, True, 0 )

		self.menu_box = Gtk.Box( orientation=Gtk.Orientation.VERTICAL )
		self.menu_box.set_size_request(150,200)

		separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)

		self.data_box = Gtk.Box( orientation=Gtk.Orientation.VERTICAL )
		self.data_box.set_size_request(350,300)

		main_wrap.pack_start( self.menu_box, False, True, 0 )
		main_wrap.pack_start( separator, False, True, 0 )
		main_wrap.pack_start( self.data_box, True, True, 0 )
		# Add to the main box to the window
		self.add( main_box )

	#---------------------------------------------------------------------------

	def set_toolbox_view(self):
		# TODO: Change style
		add_data_btn = Gtk.Button("Add URL")
		add_data_btn.set_size_request(100,0)
		add_data_btn.connect("clicked", self.btn_add_url )

		self.tool_box.pack_start( add_data_btn, False, True, 0 )

		separator = Gtk.Label("")
		separator.hide()
		self.tool_box.pack_start( separator, True, True, 0 )

		# Search
		search_bar = Gtk.Entry()
		self.tool_box.pack_start( search_bar, False, True, 0 )

		# TODO: Config button
		#add_conf_btn = Gtk.Button("Config")
		#self.tool_box.pack_start( add_conf_btn, False, True, 0 )

	#---------------------------------------------------------------------------

	def set_data_view(self):
		# Empty tree view
		self.scroll_tree = Gtk.ScrolledWindow()

		self.data_box.pack_start( self.scroll_tree, True, True, 0 )

	#---------------------------------------------------------------------------

	def set_lateral_menu_view(self):
		# Tree view
		scroll_tree = Gtk.ScrolledWindow()

		categories_data = Gtk.ListStore( str )

		self.categories = Gtk.TreeView( categories_data )
		self.categories.set_headers_visible(False)
		self.categories.connect('button-press-event' , self.category_selected)

		renderer = Gtk.CellRendererText()

		column = Gtk.TreeViewColumn("Categories", renderer, text=0)
		self.categories.append_column(column)

		scroll_tree.add( self.categories )
		self.menu_box.pack_start( scroll_tree,True,True,0 )

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

			# TODO: Right click
			#if event.button == 3:
			# Display menu

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
