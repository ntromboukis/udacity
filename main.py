#!/usr/bin/env python

import webapp2
from validate import *
from handler import Handler
from blog import BlogHandler
from post import PostHandler, NewPostHandler, EditPostHandler, deletePosts


class MainHandler(Handler):
    def get(self):
        if self.is_logged_in()[0]:
                self.render("index.html",
                            message="Welcome",
                            username=self.is_logged_in()[1][0],
                            login="Logout")
                self.render("logout.html",
                            banner="logout",
                            username=self.is_logged_in()[1][0],
                            message=", are you sure you want to log out?")
        else:
            self.render("index.html",
                        message="Welcome",
                        username="",
                        login="Sign In")
            self.render("signin.html",
                        banner="signin")

    def post(self):
        username = self.request.get('username')
        email = self.request.get('email')
        password = self.request.get('password')
        confirm_password = self.request.get('verify')
        app_engine_user = db.GqlQuery(
            "SELECT * FROM User WHERE username IN ('%s')" % username).get()

        if self.is_logged_in()[0]:
            self.logout()
            self.redirect("/")

        elif app_engine_user is not None:
            passpass = app_engine_user.hashed_password
            salt = passpass.split("|")[1]
            if self.signin(username, password, salt, passpass):
                self.redirect("/")
            else:
                self.render(
                    "signin.html",
                    password_error="incorrect username or password")

        else:
            if self.signup(username, password, confirm_password, email):
                self.render("index.html",
                            message="Welcome",
                            username=username,
                            login="Logout")
            else:
                self.render(
                    "signin.html",
                    username_error=response.get_username_error(),
                    username=response.get_username(),
                    email_error=response.get_email_error(),
                    email=response.get_email(),
                    password_error=response.get_password_error())


class AccountHandler(Handler):
    def render_front(self, subject="", content="", error="", user=""):
        user = db.GqlQuery("SELECT * FROM User")
        self.render("account.html", user=user)

    def get(self):
        self.render_front()


class CommentHandler(Handler):
    def comment(self):
        comment = self.request.get("postComment")
        print "comment %s" % comment

    def post(self):
        print "in comment post"
        self.comment()


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', BlogHandler),
    ('/newpost', NewPostHandler),
    ('/blog/([0-9]+)', PostHandler),
    ('/blog/edit/([0-9]+)', EditPostHandler),
    ('blog/comment/([0-9]+)', CommentHandler),
    ('/account', AccountHandler),
    ('/deleteall', deletePosts)

], debug=True)
