from google.appengine.ext import db
from user import User
from post import Post

class Comment(db.Model):
    '''
        Comment subclass of Model
        Properties:
                    - username(ReferenceProperty)User
                    - post(ReferenceProperty)Post
                    - comment(StringProperty)Required
                    - comment_date(DateTimeProperty)auto_now_add
    '''
    username = db.ReferenceProperty(User)
    post = db.ReferenceProperty(Post)
    comment = db.StringProperty(required=True)
    comment_date = db.DateTimeProperty(auto_now_add=True)
