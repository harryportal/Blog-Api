from blogapi import auth
from flask import g, make_response, jsonify
from blogapi.user.models import User
from flask_restful import Resource


@auth.verify_password
def verify_user(email_or_token, password):
    if not email_or_token:
        return False
    if not password:  # assumes that token was sent since password is empty
        g.token_used = True
        user = User()  # create an instance of the user class to verify token
        try:
            id = user.verify_token(email_or_token)
            g.user = User.query.get_or_404(id)
        except:
            return False
        return True
    user = User.query.filter_by(email=email_or_token).first()  # if username and password is sent
    if not user or not user.verify_password(password):
        return False
    g.user = user
    g.token_used = False
    return True


@auth.error_handler
def error():
    return make_response(jsonify({"error": 'Invalid Credentials'}), 401)

# creating a base class for resources that will need an authentication
class loginRequired(Resource):
    method_decorators = [auth.login_required]