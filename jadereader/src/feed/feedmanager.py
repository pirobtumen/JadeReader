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

import feedparser

class FeedManager:
    '''
    '''

    def __init__(self):
        self.url_manager = UrlManager()

        self.feed = {}

        self.update()

    def update_all(self):
        self.feed = {}

        url_list = url_manager.get_all_url()

        for url in url_list:
            self.download_feed( url )

    #def update_url(self, url):

    #def update_category(self, category):
    #   url_list = self.url_manager.get_category_url( category )
    #   for url in url_list:

    def download_feed(self, url):
        feed_url = url.get_feed()
        feed_list = []
        #feed_tree =

        self.feed[url.get_url()] = feed_list

    def get_categories(self):
        return self.url_manager.get_categories()

    def get_feed(self, url):
