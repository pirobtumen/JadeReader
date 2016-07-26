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

class Feed:
    '''
    '''

    def __init__(self, title, link, data):
        self.title = title
        self.link = link
        self.data = data

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------

    def get_title(self):
        return title

    def get_link(self):
        return link

    def get_data(self):
        return data

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------

    def set_title(self, title):
        self.title = title

    def set_link(self, link):
        self.link = link

    def set_data(self,data):
        self.data = data

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------

    # def parse_data(self):
