from handler import Handler
from models import Post, Comment
from validate import *

# To do - Documentation


class PostHandler(Handler):
    def get(self, post_id):
        post = Post.get_by_id(int(post_id))
        comments = Comment.all()
        comments.filter('post =', post.key())
        comments.order('-comment_date')
        print "comments in post get: %s" % comments
        for comment in comments:
            print comment
        if not post:
            self.error(404)
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
            print "in elif"
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
        p = Post.get_by_id(int(post_id))
        user = self.is_logged_in()
        update_like = self.request.get("like_checkbox")
        app_engine_user = user[1][2]
        comment = self.request.get('postComment')
        print "1comment %s" % comment
        editedComment = self.request.get("editComment")
        print "1edited comment %s" % editedComment

        if update_like == "on":
            if post_id in app_engine_user.liked:
                app_engine_user.liked.remove(post_id)
                app_engine_user.put()
                num = p.likes - 1
                p.likes = num
            else:
                app_engine_user.liked.append(post_id)
                app_engine_user.put()
                num = p.likes + 1
                p.likes = num

        if comment:
            print "comment %s" % comment
            c = Comment(username=app_engine_user.key(),
                         post=p.key(), comment=comment)
            c.put()

        if editedComment:
            print "edited comment %s" % editedComment
            c = db.get(p.key())
            c.comment = editedComment
            c.put()
            p.put()
        p.put()
        i = p.key().id()
        self.redirect("/blog/%s" % (i))


class NewPostHandler(Handler):
    def get(self):
        if self.is_logged_in()[0]:
            self.render("newpost.html",
                        login="Logout")
        else:
            #  reroutes if user is not signed in
            self.render("index.html",
                        error="You must be signed in to create a post",
                        login="Sign In")

    def post(self):
        username = self.request.cookies.get("username")
        author = db.GqlQuery("SELECT * FROM User WHERE username IN ('%s')" % username).get()
        subject = self.request.get('subject')
        content = self.request.get('content')
        checked = self.request.get('rot13_checkbox')

        if checked == "on":
            content = convert_text(content)

        if subject and content:
            p = Post(subject=subject, content=content,
                      author=author, likes=0)
            p.put()
            i = p.key().id()
            self.redirect("/blog/%s" % (i))
        else:
            error = "we need both a subject and a blog entry"
            ## FIX THIS ##
            self.render("newpost.html", subject=subject, content=content, error=error)


class EditPostHandler(Handler):
    def get(self, post_id):
        post = Post.get_by_id(int(post_id))
        if not post:
            self.error(404)
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
        p = Post.get_by_id(int(post_id))
        user = self.is_logged_in()
        if user[0] and user[1][0] == p.author:
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
                error = "we need both a subject and a blog entry"
                self.redirect("/blog")


class deletePosts(Handler):
    def get(self):
        allPosts = db.GqlQuery("SELECT * from Post")
        db.delete(allPosts)
        allUsers = db.GqlQuery("SELECT * FROM User")
        db.delete(allUsers)
        allComments = db.GqlQuery("SELECT * FROM Comment")
        db.delete(allComments)
        self.render("delete.html", message="success")
