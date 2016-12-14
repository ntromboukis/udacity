from validate import *
from handler import Handler


class AccountHandler(Handler):
    '''
        Handler subclass for the "/account" extension.
    '''
    def render_front(self, error=""):
        '''
            Params: error
            Accepts error message and renders page with all users
        '''
        user = db.GqlQuery("SELECT * FROM User")
        self.render("account.html", user=user)

    def get(self):
        '''
            Calls render_front method
        '''
        self.render_front()
