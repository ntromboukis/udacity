from google.appengine.ext import db


class Posts(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    author = db.StringProperty(required=True)
    likes = db.IntegerProperty(default=0)
    comments = db.ListProperty(str, default=None)


class User(db.Model):
    username = db.StringProperty(required=True)
    hashed_password = db.StringProperty(required=True)
    email = db.EmailProperty()
    liked = db.ListProperty(str, default=None)
