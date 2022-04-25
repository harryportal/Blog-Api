from flask_restful import Resource
from blogapi import api
from flask import jsonify, make_response, request, abort
from blogapi.auth import loginRequired
from blogapi.models import Post, PostSchema, db
from flask import g

post_schema = PostSchema()


class _Post(loginRequired):
    # create a post
    def post(self):
        post = request.get_json()
        validate = post_schema.validate(post)
        if validate:
            return jsonify({"error": validate}), 400
        new_post = Post(title=post['title'], content=post['content'], user_id=g.user.id)
        db.session.add(new_post)
        db.session.commit()
        return {"message": "Post Created"}, 201

    # get all posts for a user
    def get(self):
        posts = Post.query.filter_by(user_id=g.user.id).all()
        if posts:
            posts = post_schema.dump(posts, many=True)
            return posts
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
        post = Post.query.get(post_id)  # check if posts exist
        if post:
            return post_schema.dumps(post)
        else:
            return {"message": "Post does not exist"}, 400





api.add_resource(_Post, '/post')
api.add_resource(Post_, '/post/<int:post_id>')