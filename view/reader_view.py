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

from model import reader

# Classes
#-------------------------------------------------------------------------------

class UrlDialog( Gtk.Dialog ):
	def __init__(self, parent, categories, buttons=None):
		Gtk.Dialog.__init__(self, "New category", parent, 0 )
		self.set_default_size(150, 100)

		label_name = Gtk.Label("Name:")
		self.name = Gtk.Entry()

		label_url = Gtk.Label("URL:")
		self.url = Gtk.Entry()

		label_cat = Gtk.Label("Category:")
		cat_list = Gtk.ListStore(str)

		for category in categories:
			cat_list.append( [category] )

		self.cat = Gtk.ComboBox.new_with_model_and_entry(cat_list)
		self.cat.set_entry_text_column(0)

		#self.cat.set_activates_default(True)

		main_box = self.get_content_area()

		grid = Gtk.Grid()
		#grid.set_row_homogeneous(True)
		grid.set_row_spacing(4)
		grid.set_column_spacing(4)

		grid.add( label_name )
		grid.attach_next_to( self.name, label_name,
		Gtk.PositionType.RIGHT, 2, 1 )

		grid.attach_next_to( label_url, label_name,
		Gtk.PositionType.BOTTOM, 1, 1 )

		grid.attach_next_to( self.url, label_url,
		Gtk.PositionType.RIGHT, 2, 1 )

		grid.attach_next_to( label_cat, label_url,
		Gtk.PositionType.BOTTOM, 1, 1 )

		grid.attach_next_to( self.cat, label_cat,
		Gtk.PositionType.RIGHT, 2, 1 )

		main_box.add( grid )

		super(Gtk.Dialog, self).add_button( "Cancel", Gtk.ResponseType.CANCEL )
		super(Gtk.Dialog, self).add_button( "Save", Gtk.ResponseType.OK )

		# Set as the default action
		ok_bttn = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
		ok_bttn.set_can_default(True)
		ok_bttn.grab_default()

	#---------------------------------------------------------------------------

	def set_name(self, name):
		self.name.set_text(name)

	#---------------------------------------------------------------------------

	def set_url(self, url):
		self.url.set_text(url)
	#---------------------------------------------------------------------------

	def set_category(self, category):
		cat_entry = self.cat.get_child()
		cat_entry.set_text( category )

	#---------------------------------------------------------------------------

	def run(self):
		self.show_all()
		result = super(Gtk.Dialog, self).run()

		web_entry = None

		if result == Gtk.ResponseType.OK:
			web_entry = reader.ReaderEntry( [ self.name.get_text(), self.url.get_text(), self.cat.get_child().get_text() ] )

		self.destroy()

		return web_entry

#-------------------------------------------------------------------------------

class ReaderEntryView(Gtk.ListBoxRow):
	def __init__( self, parent, data, key ):
		Gtk.ListBoxRow.__init__(self)

		self.parent = parent
		self.entry = data
		self.key = key

		logo = Gtk.Label("Icon", valign=Gtk.Align.CENTER )
		name = Gtk.Label( self.entry.get_name() )
		url = Gtk.Label( self.entry.get_url() )

		edit_btn = Gtk.Button("Edit")
		edit_btn.connect( "clicked", self.btn_edit_entry )

		delete_btn = Gtk.Button("Delete")
		delete_btn.connect( "clicked", self.btn_del_entry )

		# Row Container
		hbox = Gtk.Box(spacing=50)

		# Add the Icon
		hbox.pack_start( logo, False, True, 10 )

		# Add the URL data
		vbox = Gtk.Box( orientation=Gtk.Orientation.VERTICAL )
		vbox.pack_start( name, True, True, 0 )
		vbox.pack_start( url, True, True, 0 )
		hbox.pack_start(vbox, True, True, 0 )

		# Buttons Box
		btn_hbox = Gtk.Box()
		hbox.pack_start( btn_hbox, False, True, 0 )

		btn_hbox.pack_start( edit_btn, False, True, 0 )
		btn_hbox.pack_start( delete_btn, False, True, 0 )

		self.add(hbox)
		self.show_all()

	def get_url(self):
		return self.entry.get_url()

	def get_name(self):
		return self.entry.get_name()

	def get_entry(self):
		return self.entry

	def btn_del_entry(self, button):
		self.parent.del_web_entry( self.key )

	def btn_edit_entry(self, button):
		self.parent.edit_web_entry( self.key, self.entry )


	"""
	get_key
	get_category
	update()
	set_data( data, key=None )
	"""

#-------------------------------------------------------------------------------
# TODO: New file

class WebView( Gtk.Window ):
	def __init__(self, parent, entry_model ):
		super(Gtk.Window,self).__init__( title="Jade Reader - " + entry_model.get_name() )
		self.set_default_size(700,400)
		self.connect("delete-event", self.close )
		self.show_all()

	def close(self, window, event ):
		self.destroy()

#-------------------------------------------------------------------------------

class ReaderView( Gtk.Window ):
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

		self.data_box = Gtk.Box( orientation=Gtk.Orientation.VERTICAL )
		self.data_box.set_size_request(350,300)

		main_wrap.pack_start( self.menu_box, False, True, 0 )
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
			url_view = WebView( self, entry )

	#---------------------------------------------------------------------------

	def open_browser(self, url):
		print( "Opening: " + url )
		webbrowser.open_new_tab("http://" + url)

	#---------------------------------------------------------------------------

	def btn_add_url(self, widget):
		dialog = UrlDialog(self, self.reader.get_category_list() )

		web_entry = dialog.run()
		if web_entry != None:
			self.add_web_entry( web_entry )

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
			new_list.add( ReaderEntryView(self,data,key) )

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

	def add_web_entry(self, web_entry):
		if web_entry.valid():
			# Update categories if neccesary
			self.add_category_to_menu( web_entry.get_category() )

			# Update model
			key = self.reader.add( web_entry )

			# Update the view
			# TODO 1: Optimize add - not reload all
			# TODO 1.1: Add the key given by the model to the WebEntryView
			self.load_category_entries( self.current_category )

		# Save data
		self.reader.save_data()

	def del_web_entry(self, web_entry_key ):
		# Delete the entry by its key
		category_empty = self.reader.delete_category_element( self.current_category, web_entry_key )

		# Update category menu
		if category_empty:
			self.load_category_menu()

		# Update the view
		self.load_category_entries( self.current_category )

		# Save data
		self.reader.save_data()

		#---------------------------------------------------------------------------

	def edit_web_entry(self, key, entry):
		dialog = UrlDialog(self, self.reader.get_category_list() )

		dialog.set_name( entry.get_name() )
		dialog.set_url( entry.get_url() )
		dialog.set_category( entry.get_category() )

		web_entry = dialog.run()
		if web_entry != None:
			# Update entry
			self.reader.update( key, web_entry )

			# Update categories
			self.load_category_menu()

			# Update current category
			self.load_category_entries( self.current_category )

			# Save data
			self.reader.save_data()
