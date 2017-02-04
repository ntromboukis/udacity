from handler import Handler
from models import Post
from validate import *


class NewPostHandler(Handler):
    '''
        Handler subclass for "/newpost" extension

        Methods: [get, post]
    '''
    def get(self):
        '''
            Checks if user is signed in
            IF user is not signed in: reroutes to "index.html"
            ELSE: renders "newpost.html"
        '''
        if self.is_logged_in()[0]:
            self.render("newpost.html",
                        login="Logout")
        else:
            #  reroutes if user is not signed in
            self.render("index.html",
                        error="You must be signed in to create a post",
                        login="Sign In")

    def post(self):
        '''
            Checks to see if user is logged in.
            Requests subject, content, rot_13checkbox from form and creates
            new post appropriately
        '''
        username = self.request.cookies.get("username")
        author = db.GqlQuery(
            "SELECT * FROM User WHERE username IN ('%s')" % username).get()
        subject = self.request.get('subject')
        content = self.request.get('content')
        checked = self.request.get('rot13_checkbox')

        if checked == "on":
            content = convert_text(content)

        if subject and content:
            p = Post(subject=subject,
                     content=content,
                     author=author,
                     likes=0)
            p.put()
            i = p.key().id()
            self.redirect("/blog/%s" % (i))
        else:
            error = "we need both a subject and a blog entry"
            self.render("newpost.html",
                        subject=subject,
                        content=content,
                        error=error)
