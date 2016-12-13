
from handler import Handler
from validate import *

# To do - Documentation


class BlogHandler(Handler):
    def render_front(self, subject="", content="",
                     error="", likes="", author="", blogs=""):
        blogs = db.GqlQuery("SELECT * FROM Post order by created desc")
        if self.is_logged_in()[0]:
            self.render(
                "blog.html", subject=subject,
                content=content, error=error,
                likes="", author="", blogs=blogs, login="Log out")
            self.render("logout.html",
                        banner="logout")
        else:
            self.render(
                "blog.html", subject=subject,
                content=content, error=error,
                likes="", author="", blogs=blogs, login="Sign In")
            self.render("signin.html",
                        banner="signin")

    def get(self):
        self.render_front()

    def post(self):
        username = self.request.get('username')
        email = self.request.get('email')
        password = self.request.get('password')
        confirm_password = self.request.get('verify')
        app_engine_user = db.GqlQuery(
            "SELECT * FROM User WHERE username IN ('%s')" % username).get()

        if self.is_logged_in()[0]:
            self.logout()
            self.redirect("/blog")

        elif app_engine_user is not None:
            passpass = app_engine_user.hashed_password
            salt = passpass.split("|")[1]
            if self.signin(username, password, salt, passpass):
                self.redirect("/blog")
            else:
                self.render(
                    "signin.html",
                    password_error="incorrect username or password")

        else:
            if self.signup(username, password, confirm_password, email):
                self.redirect("/blog")
            else:
                self.render(
                    "signin.html",
                    username_error=response.get_username_error(),
                    username=response.get_username(),
                    email_error=response.get_email_error(),
                    email=response.get_email(),
                    password_error=response.get_password_error())
