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
