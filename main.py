#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2
from google.appengine.ext import db
from validate import *

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


class Handler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t=jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))


class Posts(db.Model):
  subject = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)


class User(db.Model):
  username = db.StringProperty(required = True)
  hashed_password = db.StringProperty(required = True)


class MainHandler(Handler):
  def get(self):
    self.render("index.html")


class BlogHandler(Handler):
  def render_front(self, subject="", content="", error="", blogs=""):
    blogs = db.GqlQuery("SELECT * FROM Posts order by created desc")
    self.render("blog.html", subject=subject, content=content, error=error, blogs=blogs)

  def get(self):
      self.render_front()


class PostPage(Handler):
  def get(self, post_id):
    post = Posts.get_by_id(int(post_id))
    if not post:
      self.error(404)
    return self.render("permalink.html", post = post)


class NewPostHandler(Handler):
  def get(self):
    self.render("newpost.html")

  def post(self):
    subject = self.request.get("subject")
    content = self.request.get("content")
    checked = self.request.get("rot13_checkbox")

    if checked == "on":
      content = convert_text(content)

    if subject and content:
      p = Posts(subject = subject, content = content)
      p.put()
      i = p.key().id()
      self.redirect("/blog/%s"%(i))
    else:
      error = "we need both a subject and a blog entry"
      self.render_front(subject, content, error)


class SignupHandler(Handler):
  def get(self):
    self.render("signup.html")

  def post(self):
    username = self.request.get('username')
    email = self.request.get('email')
    password = self.request.get('password')
    confirm_password = self.request.get('verify')

    response = ValidSignup(username, email, password, confirm_password)
    response_list = response.get_list()
    if response.is_valid():
      hashed_password = make_pw_hash(username, password)
      print 'hashed_password = %s' % hashed_password
      u = User(username = username, hashed_password = hashed_password)
      self.response.headers.add_header('Set-Cookie',
        'username=%s' % str(username))
      self.response.headers.add_header('Set-Cookie',
        'hash_pass=%s' % hashed_password)
      self.response.headers.add_header('Set-Cookie',
        'logged_in=%s' % 'yes')
      self.redirect('/welcome')
    else:
      self.render("signup.html",
                username_error = response_list[0][0],
                username = response_list[0][1],
                email_error  = response_list[1][0],
                email = response_list[1][1],
                password_error = response_list[2][0])


class WelcomeHandler(Handler):
  def get(self):
    username = self.request.cookies.get('username')
    if username:
      self.render("index.html",
                  username = username)
    else:
      self.redirect('/signup')


class LogoutHandler(Handler):
  def get(self):
    username = self.request.cookies.get('username')
    if username:
      self.render("logout.html",
        username = username)

    else:
      self.redirect('index.html')




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', BlogHandler),
    ('/newpost', NewPostHandler),
    ('/blog/([0-9]+)', PostPage),
    ('/welcome?', WelcomeHandler),
    ('/signup', SignupHandler),
    ('/logout', LogoutHandler),

], debug=True)











