from flask import request
from .models import User, UserSchema, ValidateUserSchema
from blogapi import api, db
from flask import g
from flask import jsonify, make_response, abort
from blogapi.auth import loginRequired
from flask_restful import Resource
from passlib.apps import custom_app_context as password_hash
from blogapi.auth import auth



class Profile(loginRequired):
    """returns the user profile"""
    def get(self):
        User_Schema = UserSchema()
        return User_Schema.dump(g.user)

    def post(self):
        user_details = request.get_json()
        if user_details:
            check_username = User.query.filter_by(username=user_details['username']).first()
            if user_details['username'] == g.user.username:
                return {"message":"No Changes Made"}
            if check_username:
                return {"error":"Username Exists"}
            g.user.username = user_details['username']
            db.session.commit()
        else:
            return jsonify({"error":"Input required"})





class NewUser(Resource):
    @staticmethod
    def post():
        user = request.get_json()
        if not user:
            abort(400, message="No data Provided")
        # checking database to ensure email and username is unique
        error = {}
        check_user = User.query.filter_by(username=user['username']).first()
        check_mail = User.query.filter_by(email=user['email']).first()
        if check_mail:
            error["error"] = "User with Email already exist"
        if check_user:
            error["error"] = "User with Username already exist"
        if error:
            return make_response(error, 400)
        """Validate new user data"""
        Validate = ValidateUserSchema()
        error = Validate.validate(user)
        if error:
            return error, 400
        hashed_password = password_hash.hash(user['password'])
        new_user = User(username=user['username'], email=user['email'], password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": f"Account Created for {user['username']}"})

    # returns token for authentication
    @auth.login_required
    def get(self):
        if g.token_used:
            # prevents user from generating a new token with an old token
            return jsonify({'error': 'Invalid Credentials'})
        return jsonify({'token': g.user.generate_token(), 'expire': 3600})


api.add_resource(Profile, "/profile")
api.add_resource(NewUser, "/user")
