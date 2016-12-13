#!/usr/bin/env python

import webapp2
from validate import *
from handler import Handler
from blog import BlogHandler
from post import PostHandler, NewPostHandler, EditPostHandler, deletePosts
from models import Comment


class MainHandler(Handler):
    '''
        Handler subclass for "/" extension

        Methods
        - get
        - post
    '''
    def get(self):
        '''
            Checks if user is logged in and renders signup, signin, logout
            button appropriately
        '''
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
        '''
            Gets form information and applies it to signup, signin, or logout
            a user. Errors will display if information is invalid.
        '''
        username = self.request.get('username')
        email = self.request.get('email')
        password = self.request.get('password')
        confirm_password = self.request.get('verify')
        response = ValidSignup(
            username, email, password, confirm_password)
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
            if self.signup(username, password, confirm_password, email, response):
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
    '''
        Handler subclass for the "/account" extension.
    '''
    def render_front(self, error=""):
        '''
            Params: error
            Accepts error message and renders page with all users
        '''
        user = db.GqlQuery("SELECT * FROM User")
        self.render("account.html", user=user)

    def get(self):
        '''
            Calls render_front method
        '''
        self.render_front()


class EditCommentHandler(Handler):
    '''
        Handler subclass responsible for the "/blog/edit/comment/[0-9]+"
        extension.
    '''
    def get(self, comment_id):
        '''
            Params: comment_id
            Query's Comment Model using comment_id, checks if logged in user
            is author of comment and renders "editcomment.html" appropriately

            If invalid comment_id, renders "404.html"
        '''
        c = Comment.get_by_id(int(comment_id))
        if not c:
            return self.render("404.html")
        comment = c.comment
        author = c.username.username
        user = self.is_logged_in()
        if author == user[1][0]:
            self.render("editcomment.html",
                comment=comment,
                can_edit="yes")
        else:
            self.render("editcomment.html",
                can_edit="no")

    def post(self, comment_id):
        '''
            Params: comment_id
            Query's Comment Model using comment_id, requests comment and
            delete_checkbox from form. Edits comment appropriately then
            saves to db
        '''
        c = Comment.get_by_id(int(comment_id))
        comment = self.request.get("comment")
        delete_checkbox = self.request.get("delete_checkbox")
        if delete_checkbox == "on":
            c.delete()
        else:
            c.comment = comment
            c.put()
        self.redirect("/blog/%s" % c.post.key().id())


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', BlogHandler),
    ('/newpost', NewPostHandler),
    ('/blog/([0-9]+)', PostHandler),
    ('/blog/edit/([0-9]+)', EditPostHandler),
    ('/blog/edit/comment/([0-9]+)', EditCommentHandler),
    ('/account', AccountHandler),
    ('/deleteall', deletePosts)

], debug=True)
