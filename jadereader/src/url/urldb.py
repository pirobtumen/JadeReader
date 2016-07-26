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

import sqlite3

class UrlDB:
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

    def add_url(self, data):
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

    def get_url_list(self, category=None):
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
