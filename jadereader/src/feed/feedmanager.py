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

from src.feed.feed import Feed
from src.url.url import Url
import feedparser

class FeedManager:
    '''
    '''

    def download_feed(self, url_list):

        # TODO: Before download check if it already exists.
        self.feed_data = {}

        feeds = []

        for url in url_list:
            url_url = url.get_url()
            url_feed = url.get_feed()

            if url_feed is not None:
                feed = self.parse_feed( url_feed )
                feeds += feed
                #if feed:
                self.feed_data[url_url] = feed

        return feeds

    def get_all_feed(self):
        feed = []

        for key in self.feed_data:
            feed += self.feed_data[key]

        return feed

    #def get_feed(self,url):

    def parse_feed(self, feed_url):

        # feedparser issue with libxml2
        try:
            data = feedparser.parse(feed_url)
        except TypeError:
            if 'drv_libxml2' in feedparser.PREFERRED_XML_PARSERS:
                feedparser.PREFERRED_XML_PARSERS.remove('drv_libxml2')
                data = feedparser.parse(feed_url)
            else:
                raise

        feeds = []

        for post in data.entries:
            feeds.append( Feed(post.title, post.summary, post.link) )

        return feeds
