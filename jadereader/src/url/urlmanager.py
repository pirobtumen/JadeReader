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
