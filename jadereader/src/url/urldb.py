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

import sqlite3

class ReaderDB:
    def __init__(self, db_name):
        # Connect to our DataBase
        self.db_name = db_name
        self.db = sqlite3.connect( db_name )

        # Initialize tables if needed.
        self.initialze_db()

    def initialze_db(self):
        # Table name
        self.table_name = 'URL'

        # Query
        sql_query = 'CREATE TABLE IF NOT EXISTS ' + table_name + '''(
        NAME TEXT NOT NULL,
        URL TEXT PRIMARY KEY NOT NULL,
        CATEGORY TEXT NOT NULL,

        RSS TEXT
        );'''

        # Send the query
        self.db.execute( sql_query )

        # Reset
        self.reconnect()

    def reconnect(self):
        self.db.close()
        self.db = sqlite3.connect( self.db_name )

    def add_url(self, name, url, feed, category):
        sql_query = 'INSERT INTO ' + self.table_name + ' VALUES(?,?,?,?)'

        self.db.execute(sql_query, data)
        self.db.commit()

    def get_url(self, url):
        cursor = self.db.execute("SELECT * FROM " + self.table_name + " WHERE Url=?", [url] )
        return cursor

    def update(self, data):
        update_query = "UPDATE " + self.table_name + " SET name=?, url=?, category=?, rss=? WHERE url=?"
        self.db.execute( update_query, data )
        self.db.commit()

    def get_rss(self, url):
        cursor = self.db.execute("SELECT Rss FROM " + self.table_name + " WHERE Url=?", [url] )
        return cursor

    def get_url_list(self, quantity=0, category=None):
        if category == None:
            cursor = self.db.execute("SELECT * FROM " + self.table_name)
        else:
            cursor = self.db.execute("SELECT * FROM " + self.table_name + " WHERE Category=?", [category] )
        return cursor

    def del_url(self, url):
        delete_query = "DELETE FROM " + self.table_name + " WHERE Url=?"
        self.db.execute( delete_query, (url,) )
        self.db.commit()

    def get_categories(self):
        cursor = self.db.execute("SELECT DISTINCT Category FROM " + self.table_name)
        return cursor

    def del_category(self, category):
        delete_query = "DELETE FROM " + self.table_name + " WHERE Category=?"
        self.db.execute( delete_query, (category,) )
        self.db.commit()

    def rename_category(self, old_name, new_name):
        rename_query = "UPDATE " + self.table_name + " SET Category=? WHERE Category=?"
        self.db.execute( rename_query, (new_name, old_name) )
        self.db.commit()

    def close(self):
        self.db.commit()
        self.db.close()
