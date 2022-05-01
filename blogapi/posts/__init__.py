from blogapi import api
from flask import jsonify, request, abort
from blogapi.auth import loginRequired
from .models import Post, PostSchema, db, Comments, One_PostSchema
from ..user.models import UserSchema
from flask import g
from blogapi.helper import Pagination
from flask_restful import Resource
from ..user.models import User


post_schema = One_PostSchema()


class _Post(loginRequired):
    # create a post
    def post(self):
        post = request.get_json()
        validate = post_schema.validate(post)
        if validate:
            return {"error": validate}, 400
        new_post = Post(title=post['title'], content=post['content'], user=g.user.username)
        db.session.add(new_post)
        db.session.commit()
        return {"message": "Post Created"}, 201

    # get all posts for a user
    def get(self):
        posts = Post.query.filter_by(user_id=g.user.id).order_by(Post.timestamp.desc())
        if posts:
            pagination = Pagination(query=posts, schema=post_schema, request=request,
                                    resource_url='_post')
            pagination_results = pagination.paginate_query()
            return pagination_results
        else:
            return jsonify({"message": "You have no post yet"}), 200


class Post_(loginRequired):
    # edit a single post
    def put(self, post_id):
        post = Post.query.get(post_id) # check if posts exist
        if not post:
            return {"message": "Post does not exist"}, 400
        if g.user.id != post.author.id:
            abort(401)
        edited_post = request.get_json()
        validate = post_schema.validate(edited_post)
        if validate:
            return jsonify({"error": validate}), 400
        else:
            post.title = edited_post['title']
            post.content = edited_post['content']
            db.session.commit()
        return jsonify({"message": "Post Edited"}), 200

        # get all posts for a user

    # get single post
    def get(self, post_id):
        post_schema = PostSchema()
        post = Post.query.get(post_id)  # check if posts exist
        if post:
            result = post
            post = post_schema.dump(post)
            post['username'] = result.author.username
            return post
        else:
            return {"message": "Post does not exist"}, 400

class Comment(loginRequired):
    # add comment to a post
    def post(self, post_id):
        comment = request.get_json()
        post = Post.query.get(post_id)
        if post:
            comment = Comments(comment=comment['comment'], post_id=post_id, user_id=post.author.id)
            db.session.add(comment)
            db.session.commit()
        else:
            return {"message": "Post does not exist"}, 400






class All_Post(Resource):
    """ get all the posts """
    def get(self):
        user_schema = UserSchema()
        posts = Post.query.order_by(Post.timestamp.desc())
        if posts:
            pagination = Pagination(query=posts, schema=post_schema, request=request,
                                    resource_url='_post')
            pagination_results = pagination.paginate_query()
            return pagination_results
        else:
            return jsonify({"message": "No post yet"}), 200




api.add_resource(_Post, '/post')
api.add_resource(Post_, '/post/<int:post_id>')
api.add_resource(All_Post, '/posts')
api.add_resource(Comment, '/post/<int:post_id>/comment')