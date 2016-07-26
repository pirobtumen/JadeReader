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

from ..url import urlutils

class Url:
    '''
    '''

    URL_STATUS_OK = 0
    URL_STATUS_INVALID = 1
    URL_STATUS_NOFEED = 2

    def __init__(self,name,url,feed,category):
        self.name = name
        self.feed = feed
        self.category = category
        self.status = self.URL_STATUS_OK

        self.set_url( url ) # Adds http scheme

        # TODO: Check STATUS
        # self.status = self.check_status()

    # --------------------------------------------------------------------------
    # Getters
    # --------------------------------------------------------------------------

    def get_name(self):
        return self.name

    def get_url(self):
        return self.url

    def get_feed(self):
        return self.feed

    def get_category(self):
        return self.category

    # --------------------------------------------------------------------------
    # Setters
    # --------------------------------------------------------------------------

    def set_name(self, name):
        self.name = name

    def set_url(self, url):
        self.url = urlutils.url_set_scheme(url, "http://")

    def set_feed(self, feed):
        self.feed = feed

    def set_category(self, category):
        self.category = category

    # --------------------------------------------------------------------------
    # Methods
    # --------------------------------------------------------------------------

    #def check_status(self):

    def update_feed(self):
        """
        Look for <link> that contains "rss+xml" url.
        """
        web = urlutils.get_webpage(self.url)

        feed = urlutils.get_feed(web)

        self.feed = feed

        return feed
