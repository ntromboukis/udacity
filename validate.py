import codecs
import re
import random
import string
import hashlib

def convert_text(text):
  if text == None:
    return ''
  else:
    return codecs.encode(text, 'rot_13')


class ValidSignup(list):
  def __init__(self, username, email, password, confirm_password):
    self.response = list()
    self.valid = True
    self.valid_username(username)
    self.valid_email(email)
    self.valid_password(password, confirm_password)

  def valid_username(self, username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    if username and USER_RE.match(username):
      self.response.append(("", username))
    else:
      self.response.append(("Please enter a valid username",username))
      self.valid = False

  def valid_email(self, email):
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    print "DEBUGGING in valid_email"
    if EMAIL_RE.match(email) or email == "":
      self.response.append(("", email))
    else:
      self.response.append(("Non valid Email",email))
      self.valid = False

  def valid_password(self, password, confirm):
    PASS_RE = re.compile(r"^.{3,20}$")
    if password == "":
      self.response.append(("You have not entered a password",""))
      self.valid = False
    else:
      if PASS_RE.match(password) and password == confirm:
        self.response.append(("",""))

  def is_valid(self):
    return self.valid

  def get_list(self):
    return self.response



def make_salt():
  return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt=""):
  if salt == "":
      salt = make_salt()
  h = hashlib.sha256(name + pw + salt).hexdigest()
  return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
  info = h.split(',')
  v = make_pw_hash(name, pw, info[1])
  if v == h:
      return True
  else:
      return False











