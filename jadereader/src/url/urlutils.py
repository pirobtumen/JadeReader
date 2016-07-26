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

"""

URL Utilities
============================

It provides you some functions for working with URL's.

"""

import re
import requests

def url_get_scheme( url, clean=False ):
    """
    Given a URL it returns the scheme.
    If clean is 'True', it returns the scheme without '://'.
    If there is not scheme it will return 'None'.
    """

    # Regular Expression to get the scheme
    scheme_pattern = "^.*://"
    res = re.search( scheme_pattern, url )
    scheme = None

    # If something has been found get it
    if res != None:
        scheme = res.group()

        if clean:
            scheme = scheme[:-3]

    return scheme

def url_split_scheme( url, clean=False ):
    """
    Given a URL it split it in two parts, the scheme and the rest of the url.
    If clean is 'True' the scheme won't contain '://'.
    If there is not scheme it will return ( None, url ).
    """

    # Get URL and scheme
    scheme = url_get_scheme( url, clean )
    url_base = url

    # Split the URL
    if scheme != None:
        len_scheme = len(scheme)
        if clean:
            len_scheme += 3
        url_base = url[len_scheme:]

    return (scheme, url_base)

def url_set_scheme( url, scheme ):
    """
    Given a URL it changes ( or adds a new one if the URL doesn't have one )
    the scheme for the new one.
    The scheme must have '://' at the end.
    Returns the url with the new scheme.
    """
    old_scheme, url = url_split_scheme( url )
    return scheme + url

def get_webpage(url):
    """
    Get a webpage from a URL.

    Param [in] url : The URL that you want to get.

    Return: the webpage as a string.
    """
    # TODO: Handle exceptions
    return requests.get(url).text

def get_attr(attr_name, data):
    """
    Get the data from an HTML Tag.
    """
    start_pos = data.find( attr_name ) + len(attr_name)

    max_pos = len(data)

    while start_pos < max_pos and data[start_pos] != '"':
        start_pos += 1

    start_pos += 1

    end_pos = start_pos

    while end_pos < max_pos and data[end_pos] != '"':
        end_pos += 1

    return data[start_pos:end_pos]


def get_feed(data):
    """
    Scrap the feed URL from a web.

    Param[in] data : the web as string.

    Return: the feed url (string). None if it can't be find.
    """
    feed = None

    pos = data.find("rss+xml")

    if pos != -1:
        start = pos

        while data[start] != '<':
            start -= 1

        end = pos

        while data[end] != '>':
            end += 1

        end += 1

        # TODO: get href
        feed = get_attr( "href", data[start:end] )

    return feed
