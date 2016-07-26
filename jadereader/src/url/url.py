from urlutils import *

class Url:
    '''
    '''

    URL_STATUS_OK = 0
    URL_STATUS_INVALID = 1
    URL_STATUS_NOFEED = 2

    def __init__(self,name,url,feed,category):
        self.name = name
        self.url = url
        self.feed = feed
        self.status = URL_STATUS_OK
        self.category = category

        # TODO: Check STATUS

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------

    def get_name(self):
        return name

    def get_url(self):
        return url

    def get_feed(self):
        return feed

    def get_category(self):
        return category

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------

    def set_name(self, name):
        self.name = name

    def set_url(self, url):
        self.url = url

    def set_feed(self, feed):
        self.feed = feed

    def set_category(self, category):
        self.category = category

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------

    #def check_status(self):

    def update_feed(self):
        web = get_webpage(self.url)

        feed = get_feed(web)

        self.feed = feed

        return feed
