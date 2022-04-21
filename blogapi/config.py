import os

class Test_Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:112233@localhost/blogmodel'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY')