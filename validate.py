import codecs
import re
import random
import string
import hashlib
from google.appengine.ext import db


def convert_text(text):
    '''
        Converts text to rot 13 "encryption"
    '''
    if text == None:
        return ''
    else:
        return codecs.encode(text, 'rot_13')


class ValidSignup(list):
    '''
        List subclass to validate user
    '''
    def __init__(self, username, email, password, confirm_password):
        '''
            Sets initial values
        '''
        self.valid = True
        self.valid_username(username)
        self.username = ""
        self.username_error = ""
        self.valid_email(email)
        self.email = ""
        self.email_error = "Please enter a valid Email"
        self.valid_password(password, confirm_password)
        self.password_error = "Your passwords do not match"

    def user_exists(self, username):
        '''
            Params: [username]
            Checks against User Model Objects to see if username exists
            If exists sets username_error
        '''
        u = db.GqlQuery(
            "SELECT * FROM User WHERE username IN ('%s')" % username).get()
        if u == username:
            self.valid = False
        else:
            self.username_error = "That user doesn't exist"

    def valid_username(self, username):
        '''
            Params: [username]
            Checks to see if username is valid, if invalid sets username_error
        '''
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        if username and USER_RE.match(username):
            self.user_exists(username)
            self.username = username
        else:
            self.username_error = "Enter a valid username"
            self.valid = False

    def valid_email(self, email):
        '''
            Params: [email]
            Checks to see if email is valid
        '''
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        if EMAIL_RE.match(email) or email == "":
            self.email = email
        else:
            self.valid = False

    def valid_password(self, password, confirm):
        '''
            Params: [password, confirm]
            Checks to see if password matches confirm
        '''
        PASS_RE = re.compile(r"^.{3,20}$")
        if password == "":
            self.password_error = "You have not entered a password"
            self.valid = False
        elif PASS_RE.match(password) and password != confirm:
            self.password_error = "Your passwords do not match"
            self.valid = False

    def is_valid(self):
        '''
            returns self.valid()
        '''
        return self.valid

    def get_username(self):
        '''
            returns self.username
        '''
        return self.username

    def get_username_error(self):
        '''
            returns self.username_error
        '''
        return self.username_error

    def get_email(self):
        '''
            returns self.email
        '''
        return self.email

    def get_email_error(self):
        '''
            returns self.email_error
        '''
        return self.email_error

    def get_password_error(self):
        '''
            returns self.password_error
        '''
        return self.password_error


def make_salt():
    '''
        creates salt used for hashing password
    '''
    return ''.join(random.choice(string.letters) for x in xrange(5))


def make_pw_hash(name, pw, salt=""):
    '''
        Params: [name, pw, salt]
        Creates sha256 hashed password
        Returns hashed password, salt
    '''
    if salt == "":
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)


def valid_pw(name, pw):
    '''
        Params: [name, pw]
        Checks if password is valid
    '''
    h = pw
    info = pw.split('|')
    v = make_pw_hash(name, pw, info[1])
    return True if v == h else False
