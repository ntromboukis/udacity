from handler import Handler
from models import Post
from validate import *


class EditPostHandler(Handler):
    '''
        Handler subclass for "/blog/edit/([0-9]+" extension

        Methods: [get, post]
    '''
    def get(self, post_id):
        '''
            Params: post_id
            Query's Post Model using post_id
            IF no Post: renders "404.html"
            ELSE: Checks if user is author of post and renders
            "editpermalink.html" with appropriate permissions
        '''
        post = Post.get_by_id(int(post_id))
        if not post:
            return self.render("404.html")
        user = self.is_logged_in()
        if user[0] and user[1][0] == post.author.username:
            return self.render(
                "editpermalink.html",
                post=post,
                can_edit="yes")
        else:
            return self.render(
                "permalink.html",
                post=post,
                can_edit="no")

    def post(self, post_id):
        '''
            Params: post_id
            Query's Post Model using post_id
            Requests information from form, edits post appropriately
        '''
        p = Post.get_by_id(int(post_id))
        if not post:
            return self.render("404.html")
        user = self.is_logged_in()
        if user[0] and user[1][0] == p.author.username:
            subject = self.request.get("subject")
            content = self.request.get("content")
            checked = self.request.get("rot13_checkbox")
            d_checked = self.request.get("delete_checkbox")

            if checked == "on":
                content = convert_text(content)

            if subject and content:
                p.subject = subject
                p.content = content
                p.put()
                i = p.key().id()
                self.redirect("/blog/%s" % (i))

                if d_checked == "on":
                    p.delete()
                    self.redirect("/blog")

            else:
                self.redirect("/blog")
