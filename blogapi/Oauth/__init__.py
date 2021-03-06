import os
from flask import url_for
from authlib.integrations.flask_client import OAuth
from flask import Blueprint
from blogapi.user.models import User
from .edit_username import edit_google_username
from blogapi import db

gauth = Blueprint('gauth', __name__)
oauth = OAuth()

google = oauth.register(
    name='google',
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
    # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


github = oauth.register(
    name='github',
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com',
    client_kwargs={'scope': 'user'},
)

#GitHub login route
@gauth.route('/login/github')
def github_login():
    github = oauth.create_client('github')
    redirect_uri = url_for('gauth.github_authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


# GitHub authorize route
@gauth.route('/login/github/authorize')
def github_authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    user = github.get('user').json()
    # check if user is in database, else add user and generate token
    check_user = User.query.filter_by(email=user['email']).first()
    if check_user:
        token = check_user.generate_token()
        return f"You are successfully signed in using google, {token}"
    else:
        new_user = User(username=user['login'], email=user['email'])
        db.session.add(new_user)
        db.session.commit()
        token = new_user.generate_token()
        return f"You are successfully signed in using github, {token}"



# Google login route
@gauth.route('/login/google')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('gauth.google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


# Google authorize route
@gauth.route('/login/google/authorize')
def google_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    user = google.get('userinfo').json()

    # check if user is in database, else add user and generate token
    check_user = User.query.filter_by(email=user['email']).first()
    if check_user:
        token = check_user.generate_token()
        return f"You are successfully signed in using google, {token}"
    else:
        new_name = edit_google_username(user['given_name'])
        print(f"\n{user}\n")
        new_user = User(username=new_name, email=user['email'])
        db.session.add(new_user)
        db.session.commit()
        token = new_user.generate_token()
        return f"You are successfully signed in using google, {token}"