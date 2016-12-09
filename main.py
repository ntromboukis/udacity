#!/usr/bin/env python

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
        status = self.request.cookies.get('logged_in')
        print 'get status: %s' % status
        if username:
            if status == "yes":
                self.render(
                    "index.html",
                    message="Welcome",
                    username=username,
                    login="Logout")
                self.render(
                    "logout.html",
                    banner="logout",
                    username=username,
                    message=", are you sure you want to log out?")

            elif status == "no":
                self.render(
                    "index.html",
                    message="Welcome",
                    username="",
                    login="Sign In")
                self.render(
                    "signin.html",
                    banner="signin")
        else:
            self.response.headers.add_header(
                'Set-Cookie',
                'new=yes')
            self.render(
                "index.html",
                message="Welcome",
                username="",
                login="Signup")
            self.render(
                "signup.html",
                banner="signup")

    def post(self):
        first_time = self.request.cookies.get('new')
        if first_time == "yes":
            username = self.request.get('username')
            email = self.request.get('email')
            password = self.request.get('password')
            confirm_password = self.request.get('verify')

            response = ValidSignup(username, email, password, confirm_password)
            if response.is_valid():
                hashed_password = make_pw_hash(username, password)
                u = User(username=username, hashed_password=hashed_password)
                u.put()
                self.response.headers.add_header('Set-Cookie',
                                                 'new=no')
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

        else:
            username = self.request.cookies.get('username')
            if username:
                status = self.request.cookies.get('logged_in')
                if status == "yes":
                    self.response.headers.add_header(
                        'Set-Cookie', 'logged_in=%s' % 'no')
                    self.render(
                        "index.html",
                        username=username,
                        message=", your are logged out")
                    self.redirect("/")

                elif status == "no":
                        print 'in elif no'
                        password = self.request.get('password')
                        app_engine_user = db.GqlQuery(
                            "SELECT * FROM User WHERE username IN ('%s')" % username).get()
                        passpass = app_engine_user.hashed_password
                        salt = passpass.split("|")[1]
                        print salt
                        hashed_password = make_pw_hash(username, password, salt)
                        if hashed_password == passpass:
                            print 'in hash == pass'
                            self.response.headers.add_header(
                                'Set-Cookie',
                                'username=%s' % str(username))
                            self.response.headers.add_header(
                                'Set-Cookie',
                                'hash_pass=%s' % str(hashed_password))
                            self.response.headers.add_header(
                                'Set-Cookie',
                                'logged_in=%s' % 'yes')
                            self.redirect("/")
                        else:
                            self.render(
                                "signin.html",
                                password_error="Not correct password")
                else:
                    self.redirect("/")
            else:
                self.redirect("/")


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


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', BlogHandler),
    ('/newpost', NewPostHandler),
    ('/blog/([0-9]+)', PostPage),
    ('/account', AccountHandler),
    ('/deleteall', deletePosts)

], debug=True)
