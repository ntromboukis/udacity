from handler import Handler
from models import Post, Comment
from validate import *


class PostHandler(Handler):
    '''
        Handler subclass for "/blog/([0-9]+" extension

        Methods: [get, post]
    '''
    def get(self, post_id):
        '''
            Params: post_id

            Query:
                Post Model by post_id
                Comment Model by post.key()
            Displays all comments attached to a particular Post.
        '''
        post = Post.get_by_id(int(post_id))
        if not post:
            self.redirect("/blog")
        comments = Comment.all()
        comments.filter('post =', post.key())
        comments.order('-comment_date')
        if not post:
            self.error(404)
            return self.render("404.html")
        user = self.is_logged_in()
        if user[0] and user[1][0] == post.author.username:
            return self.render(
                "permalink.html",
                post=post,
                comments=comments,
                username=user[1][0],
                can_comment="yes",
                can_edit="yes",
                edit_link="/blog/edit/%s" % post.key().id())
        elif user[0]:
            app_engine_user = db.GqlQuery(
                "SELECT * FROM User WHERE username IN ('%s')"
                % user[1][0]).get()
            if post_id in app_engine_user.liked:
                return self.render(
                    "permalink.html",
                    post=post,
                    status="Like",
                    liked="yes",
                    comments=comments,
                    can_comment="yes")
            else:
                return self.render(
                    "permalink.html",
                    post=post,
                    status="Like",
                    liked="no",
                    comments=comments,
                    can_comment="yes")
        else:
            return self.render(
                "permalink.html",
                post=post,
                can_comment="no",
                comments=comments)

    def post(self, post_id):
        '''
            Params: [post_id]
            Description:
            Updates db if user likes a post, adds comment if present,
            links to page for user to edit or delete their comment.
        '''
        post = Post.get_by_id(int(post_id))
        if not post:
            self.error(404)
            self.redirect("/blog")
        user = self.is_logged_in()
        update_like = self.request.get("like_checkbox")
        app_engine_user = user[1][2]
        comment = self.request.get('postComment')
        editedComment = self.request.get("editComment")

        if update_like == "on":
            if post_id in app_engine_user.liked:
                app_engine_user.liked.remove(post_id)
                app_engine_user.put()
                num = post.likes - 1
                post.likes = num
            else:
                app_engine_user.liked.append(post_id)
                app_engine_user.put()
                num = post.likes + 1
                post.likes = num

        if comment:
            c = Comment(username=app_engine_user.key(),
                        post=post.key(), comment=comment)
            c.put()

        if editedComment:
            c = db.get(post.key())
            c.comment = editedComment
            c.put()
            post.put()
        post.put()
        i = post.key().id()
        self.redirect("/blog/%s" % (i))
