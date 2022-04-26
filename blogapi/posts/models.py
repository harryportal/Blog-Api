from blogapi import db, ma
from marshmallow import fields, validate
from blogapi.user.models import UserSchema


class Post(db.Model):
    __tablename__ = 'Post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.TIMESTAMP)
    comments = db.relationship('Comments', backref='post', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)


class Comments(db.Model):
    __tablename__ = 'Comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('Post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

class PostSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    content = fields.String(required=True, validate=validate.Length(min=5, max=25))
    user = fields.Nested(UserSchema, only=['id', 'username', 'email'])