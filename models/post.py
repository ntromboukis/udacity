from google.appengine.ext import db
from user import User


class Post(db.Model):
    '''
        Post subclass of Model
        Properties:
                    - subject(StringProperty)Required
                    - content(StringProperty)Required
                    - post_date(DateTimeProperty)auto_now_add
                    - author(ReferenceProperty)User
                    - likes(IntegerProperty)
    '''
    subject = db.StringProperty(required=True)
    content = db.StringProperty(required=True)
    post_date = db.DateTimeProperty(auto_now_add=True)
    author = db.ReferenceProperty(User)
    likes = db.IntegerProperty(default=0)
