from google.appengine.ext import db


class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    post_date = db.DateTimeProperty(auto_now_add=True)
    author = db.StringProperty(required=True)
    likes = db.IntegerProperty(default=0)


class User(db.Model):
    username = db.StringProperty(required=True)
    hashed_password = db.StringProperty(required=True)
    email = db.EmailProperty()
    liked = db.ListProperty(str, default=None)


class Comment(db.Model):
    username = db.ReferenceProperty(User)
    post = db.ReferenceProperty(Post)
    comment = db.StringProperty(required=True)
    comment_date = db.DateTimeProperty(auto_now_add=True)
