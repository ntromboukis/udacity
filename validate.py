import codecs
import re
import random
import string
import hashlib
from google.appengine.ext import db


def convert_text(text):
    if text == None:
        return ''
    else:
        return codecs.encode(text, 'rot_13')


class ValidSignup(list):
    def __init__(self, username, email, password, confirm_password):
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
        u = db.GqlQuery(
            "SELECT * FROM User WHERE username IN ('%s')" % username).get()
        if u == username:
            self.valid = False
            # return True
        else:
            self.username_error = "That user doesn't exist"
            # return False

    def valid_username(self, username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        if username and USER_RE.match(username):
            self.user_exists(username)
            self.username = username
        else:
            self.username_error = "Enter a valid username"
            self.valid = False

    def valid_email(self, email):
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        if EMAIL_RE.match(email) or email == "":
            self.email = email
        else:
            self.valid = False

    def valid_password(self, password, confirm):
        PASS_RE = re.compile(r"^.{3,20}$")
        if password == "":
            self.password_error = "You have not entered a password"
            self.valid = False
        elif PASS_RE.match(password) and password != confirm:
            self.password_error = "Your passwords do not match"
            self.valid = False

    def is_valid(self):
        return self.valid

    def get_username(self):
        return self.username

    def get_username_error(self):
        return self.username_error

    def get_email(self):
        return self.email

    def get_email_error(self):
        return self.email_error

    def get_password_error(self):
        return self.password_error


def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))


def make_pw_hash(name, pw, salt=""):
    if salt == "":
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    print 'result from make_pw_hash: %s|%s\n\n' % (h, salt)
    return '%s|%s' % (h, salt)


def valid_pw(name, pw):
    h = pw
    info = pw.split('|')
    v = make_pw_hash(name, pw, info[1])
    if v == h:
        return True
    else:
        return False
