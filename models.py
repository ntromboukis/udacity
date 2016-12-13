from google.appengine.ext import db


class User(db.Model):
    username = db.StringProperty(required=True)
    hashed_password = db.StringProperty(required=True)
    email = db.EmailProperty()
    liked = db.ListProperty(str, default=None)


class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.StringProperty(required=True)
    post_date = db.DateTimeProperty(auto_now_add=True)
    author = db.ReferenceProperty(User)
    likes = db.IntegerProperty(default=0)


class Comment(db.Model):
    username = db.ReferenceProperty(User)
    post = db.ReferenceProperty(Post)
    comment = db.StringProperty(required=True)
    comment_date = db.DateTimeProperty(auto_now_add=True)
