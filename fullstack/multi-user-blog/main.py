#!/usr/bin/env python

import webapp2
from handlers import *


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', BlogHandler),
    ('/newpost', NewPostHandler),
    ('/blog/([0-9]+)', PostHandler),
    ('/blog/edit/([0-9]+)', EditPostHandler),
    ('/blog/edit/comment/([0-9]+)', EditCommentHandler),
    ('/account', AccountHandler)

], debug=True)
