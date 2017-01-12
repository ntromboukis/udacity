from validate import *
from handler import Handler


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
