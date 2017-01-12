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
