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
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Posts(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    author = db.StringProperty()
    likes = db.IntegerProperty()


class User(db.Model):
    username = db.StringProperty(required=True)
    hashed_password = db.StringProperty(required=True)
    email = db.EmailProperty()
    # liked = db.ListProperty() # Stores list of post.id that this user likes


class deletePosts(Handler):
    def get(self):
        allPosts = db.GqlQuery("SELECT * from Posts")
        db.delete(allPosts)
        allUsers = db.GqlQuery("SELECT * FROM User")
        db.delete(allUsers)
        self.render("delete.html", message="success")


class MainHandler(Handler):
    def get(self):
        username = self.request.cookies.get('username')
        if username:
            hashed_password = self.request.cookies.get('hash_pass')
            app_engine_user = db.GqlQuery(
                "SELECT * FROM User WHERE username IN ('%s')" % username).get()
            passpass = app_engine_user.hashed_password
            if hashed_password == passpass:
                self.render("index.html",
                            message="Welcome",
                            username=username,
                            login="Logout")
                self.render("signup.html",
                            message="Are you sure you want to log out?")
            else:
                self.render("index.html",
                            message="Welcome",
                            username="",
                            login="Signup")
                self.render("signup.html")
        else:
            self.render("index.html",
                        message="Welcome",
                        username="")


class BlogHandler(Handler):
    def render_front(self, subject="", content="", error="", blogs=""):
        blogs = db.GqlQuery("SELECT * FROM Posts order by created desc")
        self.render("blog.html", subject=subject,
                    content=content, error=error, blogs=blogs)

    def get(self):
        self.render_front()


class AccountHandler(Handler):
    def render_front(self, subject="", content="", error="", user=""):
        user = db.GqlQuery("SELECT * FROM User")
        self.render("account.html", user=user)

    def get(self):
        self.render_front()


class PostPage(Handler):
    def get(self, post_id):
        post = Posts.get_by_id(int(post_id))
        if not post:
            self.error(404)
        return self.render("permalink.html", post=post)


class NewPostHandler(Handler):
    def get(self):
        username = self.request.cookies.get("username")
        if username:
            self.render("newpost.html")
        else:
            self.render("newpost.html",
                        error="You must be signed in to create a post")

    def post(self):
        username = self.request.cookies.get("username")
        subject = self.request.get("subject")
        content = self.request.get("content")
        checked = self.request.get("rot13_checkbox")

        if checked == "on":
            content = convert_text(content)

        if subject and content:
            p = Posts(subject=subject, content=content,
                      author=username, likes=0)
            p.put()
            i = p.key().id()
            self.redirect("/blog/%s" % (i))
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
        if response.is_valid():
            hashed_password = make_pw_hash(username, password)
            # print 'hashed_password from signupHandler = %s' % hashed_password
            u = User(username=username, hashed_password=hashed_password)
            u.put()
            self.response.headers.add_header('Set-Cookie',
                                             'username=%s' % str(username))
            self.response.headers.add_header('Set-Cookie',
                                             'hash_pass=%s' % hashed_password)
            self.response.headers.add_header('Set-Cookie',
                                             'logged_in=%s' % 'yes')
            self.redirect('/')
        else:
            self.render("signup.html",
                        username_error=response.get_username_error(),
                        username=response.get_username(),
                        email_error=response.get_email_error(),
                        email=response.get_email(),
                        password_error=response.get_password_error())


class LogoutHandler(Handler):
    def get(self):
        username = self.request.cookies.get('username')
        if username:
            hashed_password = self.request.cookies.get('hash_pass')
            app_engine_user = db.GqlQuery(
                "SELECT * FROM User WHERE username IN ('%s')" % username).get()
            passpass = app_engine_user.hashed_password
            if hashed_password == passpass:
                self.response.headers.add_header(
                    'Set-Cookie', 'hash_pass=%s' % 'hunter2')
                self.render("index.html",
                            message='You are now logged out',
                            username=username)
            else:
                self.redirect("/")
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', BlogHandler),
    ('/newpost', NewPostHandler),
    ('/blog/([0-9]+)', PostPage),
    ('/signup', SignupHandler),
    ('/logout', LogoutHandler),
    ('/account', AccountHandler),
    ('/deleteall', deletePosts)

], debug=True)
