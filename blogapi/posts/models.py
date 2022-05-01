from blogapi import db, ma
from marshmallow import fields, validate
from blogapi.user.models import UserSchema
from datetime import datetime


class Post(db.Model):
    __tablename__ = 'Post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow().strftime('%Y-%m-%d %I:%M'))
    comments = db.relationship('Comments', backref='post', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    username = db.Column(db.String)

    def __repr__(self):
        return f'Title:{self.title}, Content:{self.content}, Comments:{self.comments}'


class Comments(db.Model):
    __tablename__ = 'Comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('Post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __repr__(self):
        return self.comment

class CommentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    comment = fields.String(required=True)




class PostSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    content = fields.String(required=True, validate=validate.Length(min=5))
    timestamp = fields.String()
    comments = fields.Nested(CommentSchema, many=True)


class One_PostSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    content = fields.String(required=True, validate=validate.Length(min=5))
    timestamp = fields.String()
    username = fields.String()

