from blogapi import db, ma
from jwt import encode, decode
import os
from dotenv import load_dotenv
from marshmallow import fields, validate
from passlib.apps import custom_app_context as password_hash
from datetime import datetime, timedelta

load_dotenv()


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comments', backref='user', lazy=True)

    def generate_token(self, expire_time=30):
        token = encode({"user_id": self.id, 'exp': datetime.utcnow() + timedelta(seconds=expire_time)},
                       os.getenv('SECRET_KEY'), algorithm='HS256')
        return token

    def verify_token(self, token):
        try:
            validate = decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        except:
            return False
        return validate['user_id'] if validate else False

    def verify_password(self, password):
        verify = password_hash.verify(password, self.password_hash)
        return verify


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)  # makes it a read only data
    username = fields.String(required=True, validate=validate.Length(min=5, max=12))
    email = fields.Email(required=True)


class ValidateUserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)  # makes it a read only data
    username = fields.String(required=True, validate=validate.Length(min=5, max=12))
    email = fields.Email(required=True)
    password = fields.String(required=True)
