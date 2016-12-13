from google.appengine.ext import db


class User(db.Model):
    '''
        User subclass of Model
        Properties:
                    - username(StringProperty)Required
                    - hashed_password(StringProperty)Required
                    - email(EmailProperty)
                    - liked(ListProperty)String
    '''
    username = db.StringProperty(required=True)
    hashed_password = db.StringProperty(required=True)
    email = db.EmailProperty()
    liked = db.ListProperty(str, default=None)


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
