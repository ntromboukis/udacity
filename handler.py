
import os
import webapp2
from validate import *
from models import User
import jinja2


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    '''
        Handler Class
        Methods:
        write, render_str, render, is_logged_in, logout, signup, signin
    '''
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def is_logged_in(self):
        '''
            - Gets username, logged_in, hash_pass from cookies
            - Checks if cookie credentials match db credentials
            for the user
            - Returns tuple of if credentials check out, username,
            hash_pass (pulled from cookies), app_engine_user from
            db if credentials True
        '''
        username = self.request.cookies.get('username')
        logged_in = self.request.cookies.get('logged_in')
        hash_pass = self.request.cookies.get('hash_pass')
        app_engine_user = db.GqlQuery(
            "SELECT * FROM User WHERE username IN ('%s')" % username).get()
        try:
            passpass = app_engine_user.hashed_password
        except AttributeError:
            return (False, [username, hash_pass])

        if logged_in == "yes" and passpass == hash_pass:
            return (True, [username, hash_pass, app_engine_user])
        else:
            return (False, [username, hash_pass])

    def logout(self):
        '''
            Sets logged_in cookie to "no"
        '''
        self.response.headers.add_header(
            'Set-Cookie', 'logged_in=%s' % 'no')

    def signup(self, username, password, confirm_password, email, response):
        '''
            - Gets information from signup modal and if valid
            creats a new user and stores it into the db.
            - Sets cookies to username, hash_pass, and logged_in
            if valid information.
            Returns
            - True if successful
            - False if unsuccessful
        '''
        if response.is_valid():
            hashed_password = make_pw_hash(username, password)
            u = User(username=username,
                     hashed_password=hashed_password)
            u.put()
            self.response.headers.add_header(
                'Set-Cookie',
                'username=%s' % str(username))
            self.response.headers.add_header(
                'Set-Cookie',
                'hash_pass=%s' % hashed_password)
            self.response.headers.add_header(
                'Set-Cookie',
                'logged_in=%s' % 'yes')
            return True
        else:
            return False

    def signin(self, username, password, salt, hashed_password):
        '''
            Parameters: username, password, salt, passpass
            ** hashed_password is User.hashed_password **

            - Creates hashed password using password and salt
            IF hashed_password == passpass sets cookies username,
            passpass, logged_in
            Returns True
            ELSE
            Returns False
        '''
        passpass = make_pw_hash(username, password, salt)
        if hashed_password == passpass:
            self.response.headers.add_header(
                'Set-Cookie',
                'username=%s' % str(username))
            self.response.headers.add_header(
                'Set-Cookie',
                'hash_pass=%s' % str(passpass))
            self.response.headers.add_header(
                'Set-Cookie',
                'logged_in=%s' % 'yes')
            return True
        else:
            return False
