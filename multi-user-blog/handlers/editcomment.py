from handler import Handler
from models import Comment


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
        if not c:
            return self.render("404.html")
        comment = self.request.get("comment")
        delete_checkbox = self.request.get("delete_checkbox")
        if delete_checkbox == "on":
            c.delete()
        else:
            c.comment = comment
            c.put()
        self.redirect("/blog/%s" % c.post.key().id())
