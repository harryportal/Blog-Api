import os

class Test_Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:112233@localhost/blogmodel'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PAGINATION_SIZE_PER_PAGE = 5
    SERVER_NAME = 'localhost:5000'
    GOOGLE_CLIENT_ID = os.getenv('CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('CLIENT_SECRET')

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PAGINATION_SIZE_PER_PAGE = 10
    GOOGLE_CLIENT_ID = os.environ.get('CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('CLIENT_SECRET')