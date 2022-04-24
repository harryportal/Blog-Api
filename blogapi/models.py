from blogapi import db, ma
from jwt import encode, decode
import os
from marshmallow import fields, validate
from passlib.apps import custom_app_context as password_hash


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comments', backref='user', lazy=True)

    def generate_token(self):
        token = encode({"user_id": self.id}, os.environ.get('SECRET_KEY'), algorithm='HS256')
        return token

    def verify_token(self, token):
        try:
            validate = decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
        except:
            return False
        return validate['user_id'] if validate else False

    def verify_password(self, password):
        verify = password_hash.verify(password, self.password_hash)
        return verify





class Post(db.Model):
    __tablename__ = 'Post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    post = db.Column(db.String, nullable=False)
    comments = db.relationship('Comments', backref='post', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)


class Comments(db.Model):
    __tablename__ = 'Comments'
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
    password = fields.String(required=True)
    posts = fields.Nested('TodoSchema', many=True)  # for a one to many relationship

class PostSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    todo_name = fields.String(required=True)
    completed = fields.Boolean()
    user_todo = fields.Nested(UserSchema, only=['id', 'username', 'email'], required=True)