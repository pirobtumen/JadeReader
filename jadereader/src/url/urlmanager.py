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

class UrlManager:
    '''
    '''

    def __init__(self):
        self.db_name = "JadeReaderDB"
        self.db = ReaderDB( self.db_name )

    # --------------------------------------------------------------------------
    # URL
    # --------------------------------------------------------------------------

    def add_url(self, url):

    def get_url(self, url):

    def update_url(self, url):

    def del_url(self,url):

    # --------------------------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------------------------

    def get_category(self, category):

    def get_categories(self):
        return self.db.get_categories()

    def rename_category(self, old_name, new_name):
        self.db.rename_category(old_name,new_name)

    def del_category(self,category):
