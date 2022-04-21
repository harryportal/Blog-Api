from blogapi import db, ma
from jwt import encode, decode
import os
from marshmallow import fields, validate


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comments', backref='post', lazy=True)

    def generate_token(self):
        token = encode({"user_id": self.id}, os.environ.get('SECRET_KEY'), algorithm='HS256')
        return token

    def validate_token(self, token):
        try:
            validate = decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
        except:
            return False
        return True if validate['user_id'] == self.id else False


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    post = db.Column(db.String, nullable=False)
    comments = db.relationship('Comments', backref='post', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('Post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)  # makes it a read only data
    username = fields.String(required=True, validate=validate.Length(min=5, max=12))
    email = fields.Email(required=True)


class ValidateUserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)  # makes it a read only data
    username = fields.String(required=True, validate=validate.Length(min=5, max=12))
    email = fields.Email(required=True)
    password_hash = fields.String(required=True)
    posts = fields.Nested('TodoSchema', many=True)  # for a one to many relationship

class PostSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    todo_name = fields.String(required=True)
    completed = fields.Boolean()
    user_todo = fields.Nested(UserSchema, only=['id', 'username', 'email'], required=True)