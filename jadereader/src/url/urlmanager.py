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
        self.db = UrlDB( self.db_name )

    # --------------------------------------------------------------------------
    # URL
    # --------------------------------------------------------------------------

    def add_url(self, url):
        """
        @param [in] url : Url Object
        """
        data = (url.get_name(), url.get_url(), url.get_feed(), url.get_category())
        self.db.add_url( data )

    def get_url(self, url):
        """
        @param [in] url : string
        """
        data = self.db.get_url(url)
        return Url(data)

    def update_url(self, url):
        data = (url.get_name(), url.get_url(), url.get_feed(), url.get_category())
        self.db.update_url(data)

    def del_url(self, url):
        """
        @param [in] url : string
        """

        self.db.del_url(url)

    # --------------------------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------------------------

    def get_category(self, category):
        url_data = self.db.get_url_list(category)
        urls = []

        for url in url_data:
            urls.append( Url(url) )

        return urls

    def get_categories(self):
        return self.db.get_categories()

    def rename_category(self, old_name, new_name):
        self.db.rename_category(old_name,new_name)

    def del_category(self,category):
        self.db.del_category(category)
